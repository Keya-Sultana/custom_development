# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.exceptions import UserError
from odoo import models, fields, api, SUPERUSER_ID


class StockGateIn(models.Model):
    _name = 'stock.gate.in'
    _inherit = ['stock.gate.in', 'mail.thread']


    responsible = fields.Many2one('res.users', string='Responsible', required=True, readonly=True,
                                  default=lambda self: self.env.user, track_visibility='onchange')
    gate_passno = fields.Many2one('stock.gate.out', string='Gate Pass No.')
    attention_id = fields.Many2one('res.users', string='Attention Person')
    date = fields.Date(string="Date", readonly=True, states={'draft': [('readonly', False)]}, required=False)
    entry_date = fields.Datetime('Entry Date', readonly=True, default=fields.Datetime.now)
    supplier_phone = fields.Char("Supplier's Phone No")
    carried_phone = fields.Char("Carried By Phone No")

    gate_type = fields.Selection([('asset', "Asset Item"), ('inventory', "Inventory Item"), ('returnable', "Returnable Item")], readonly=True, string='Gate in type',
                                     required=False, states={'draft': [('readonly', False)]}, track_visibility='onchange')


    receive_type = fields.Selection([('lc', "LC"), ('others', "Others")], readonly=True,
                                    required=False, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    challan_bill_no = fields.Char('Challan Bill No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                                  required=False)
    truck_no = fields.Char('Truck/Vehicle No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                            required=False)
    create_by = fields.Char('Carried By', size=100, readonly=True, states={'draft': [('readonly', False)]},
                             required=False)
    received = fields.Char('To Whom Received', size=100, readonly=True, states={'draft': [('readonly', False)]}, required=False)

    stock_line_ids = fields.One2many('stock.product.line', 'parent_id', required=True, readonly=True,
                                        states={'draft': [('readonly', False)]})
    reference_in = fields.Char("Reference")

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirm', "Confirm"),
        ('receive', "Received"),
        ('done', "Done"),
    ], default='draft', track_visibility='onchange')


    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.supplier_phone = self.partner_id.phone

    @api.multi
    def action_confirm(self):
        self.state = 'confirm'

        for gate in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_inventory.group_yuko_security')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                gate.message_post(body="Please receive this product(s).",
                                    partner_ids=partner_ids)

    @api.multi
    def action_receive(self):
        self.state = 'receive'

        for gate in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('stock.group_stock_user')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                gate.message_post(body="This product(s) received.",
                                    partner_ids=partner_ids)

    @api.multi
    def action_done(self):
        self.state = 'done'


class StockProductLine(models.Model):
    _name = 'stock.product.line'
    _description = 'Product'
    _order = "date_planned desc"

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                change_default=True)
    date_planned = fields.Date(string='Scheduled Date', index=True)
    product_uom = fields.Many2one('product.uom', 'Unit of Measure', readonly=True)
    # product_uom = fields.Many2one(related='product_id.uom_id',comodel='product.uom',string='UOM',store=True, required=True)
    price_unit = fields.Float(related='product_id.standard_price',string='Unit Price',store=True)
    product_qty = fields.Float(string='Quantity', required=True)
    parent_id = fields.Many2one('stock.gate.in',
                                string='Gate In')

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirm', "Confirm"),
    ], default='draft')

    ####################################################
    # Business methods
    ####################################################

    @api.one
    @api.constrains('product_qty')
    def _check_product_qty(self):
        if self.product_qty < 0:
            raise UserError('You can\'t give negative value!!!')

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        self.name = self.product_id.display_name

        return result

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for po in self:

            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('purchase.group_purchase_manager','stock.group_stock_user')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                po.message_post(body="You have been assigned to approve.",
                                partner_ids=partner_ids)
        return res

    @api.multi
    def button_approve(self, force=False):
        res = super(PurchaseOrder, self).button_approve()
        for po in self:
            stock_req = po._create_stock_gate()
            if stock_req:
                po._create_stock_pro_line(stock_req[0].id or False)

                # Send Group Notification
                partner_ids = []
                grp = self.env.ref('stock.group_stock_user')
                for u in grp.users:
                    if u.partner_id:
                        partner_ids.append(u.partner_id.id)

                if partner_ids:
                    po.message_post(body="You have been assigned to receive goods.",
                                    partner_ids=partner_ids)
        return res

    @api.multi
    def _create_stock_gate(self):
        gate_obj = self.env['stock.gate.in']

        values = {
            'reference_in': self.name,
            'partner_id': self.partner_id.id,
        }

        return gate_obj.create(values)

    @api.multi
    def _create_stock_pro_line(self, req_id):
        pur_line_obj = self.env['stock.product.line']

        for line in self.order_line:
            values = {
                'parent_id': req_id,
                'product_id': line.product_id.id,
                'name': line.name or False,
                'product_qty': line.product_qty or False,
                'product_uom': line.product_uom.id or False,
            }
            pur_line_obj.create(values)
