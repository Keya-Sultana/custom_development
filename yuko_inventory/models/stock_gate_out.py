# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class StockGateOut(models.Model):
    _name = 'stock.gate.out'
    _inherit = ['stock.gate.out', 'mail.thread']


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char(string='Gate pass num', index=False, readonly=True)

    receive_type = fields.Selection([('asset', "Asset Item"), ('inventory', "Inventory Item"), ('returnable', "Returnable Item")], readonly=True, string='Gate pass type',
                                     required=False, states={'draft': [('readonly', False)]}, track_visibility='onchange')

    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True,
                              compute_sudo=True, store=True, default=lambda self: self.env.uid, readonly=True)
    # responsible = fields.Many2one('res.users', string='Responsible', required=True, readonly=True,
    #                               default=lambda self: self.env.user, track_visibility='onchange')

    employee_id = fields.Many2one('hr.employee', string='Generate by', index=True, readonly=True,
                                  default=_default_employee)
    depart_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department',
                                readonly=True, store=True)
    date = fields.Datetime(string="Date", readonly=True, states={'draft': [('readonly', False)]}, required=False)

    issue_id = fields.Many2one('res.partner', string='Issued to', readonly=True,
                                 states={'draft': [('readonly', False)]})

    inventory_outno = fields.Char("Inventory Out No")
    reference_out = fields.Char("Reference")
    gate_out_note = fields.Text("Note")
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 change_default=True, index=True, track_visibility='always')

    # receive_type = fields.Selection([('lc', "LC"), ('others', "Others")], readonly=True,
    #                                required=False, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    challan_bill_no = fields.Char('Challan Bill No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                                   required=False)
    truck_no = fields.Char('Truck/Vehicle No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                             required=False)
    create_by = fields.Char('Carried By', size=100, readonly=True, states={'draft': [('readonly', False)]},
                             required=False)
    received = fields.Char('To Whom Received', size=100, readonly=True, states={'draft': [('readonly', False)]}, required=False)
    out_line_ids = fields.One2many('stock.out.line', 'parent_id', required=True, readonly=True,
                                     states={'draft': [('readonly', False)]})

    state = fields.Selection([
        ('draft', "Draft"),
        ('approval', "Admin Approval"),
        ('check', "Security Check"),
        ('done', "Done"),
        ('reject', "Reject"),
    ], default='draft', track_visibility='onchange')



    @api.onchange('employee_id')
    def _onchange_employee(self):
        self.depart_id = self.employee_id.department_id

    @api.multi
    def action_confirm(self):
        for go in self:
            go.state = 'approval'

            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_inventory.group_yuko_admin_manager')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                go.message_post(body="You have been assigned to approve.",
                                partner_ids=partner_ids)

    @api.multi
    def action_approval(self):
        for go in self:
            go.state = 'check'

            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_inventory.group_yuko_security')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                go.message_post(body="You have been assigned to check.",
                                partner_ids=partner_ids)

    @api.multi
    def action_check(self):
        self.state = 'done'

    @api.multi
    def action_reject(self):
        for go in self:
            go.state = 'reject'

            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('stock.group_stock_user')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                go.message_post(body="Your gate pass rejected.",
                                partner_ids=partner_ids)

class StockOutLine(models.Model):
    _name = 'stock.out.line'
    _description = 'Product'
    _order = "date_planned desc"

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                change_default=True)
    date_planned = fields.Date(string='Scheduled Date', index=True)
    product_uom = fields.Many2one(related='product_id.uom_id',comodel='product.uom',string='UOM',store=True, required=True)
    product_qty = fields.Float(string='Quantity', required=True)
    remark = fields.Text(string='Remark')
    parent_id = fields.Many2one('stock.gate.out',
                                string='Gate Out')

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

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            stock_req = so._create_stock_gate()
            if stock_req:
                so._create_stock_pro_line(stock_req[0].id or False)
        return res

    @api.multi
    def _create_stock_gate(self):
        gate_obj = self.env['stock.gate.out']

        values = {
            'reference_out': self.name,
            'partner_id': self.partner_id.id,
        }

        return gate_obj.create(values)

    @api.multi
    def _create_stock_pro_line(self, req_id):
        pur_line_obj = self.env['stock.out.line']

        for line in self.order_line:
            values = {
                'parent_id': req_id,
                'product_id': line.product_id.id,
                'name': line.name or False,
                'product_qty': line.product_uom_qty or False,
                'product_uom': line.product_uom.id or False,
            }
            pur_line_obj.create(values)