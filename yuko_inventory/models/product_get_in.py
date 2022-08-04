# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class ProductGateIn(models.Model):
    _inherit = 'product.gate.in'

    responsible = fields.Many2one('res.users', string='Responsible', required=True, readonly=True,
                                  default=lambda self: self.env.user, track_visibility='onchange')
    gate_entry = fields.Many2one('hr.employee', string='Attention Person')
    date = fields.Date(string="Date", readonly=True, states={'draft': [('readonly', False)]}, required=False)
    entry_date = fields.Datetime('Entry Date', readonly=True, default=fields.Datetime.now)
    supplier_phone = fields.Char("Supplier's Phone No")
    carried_phone = fields.Char("Carried By Phone No")

    receive_type = fields.Selection([('lc', "LC"), ('others', "Others")], readonly=True,
                                    required=False, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    challan_bill_no = fields.Char('Challan Bill No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                                  required=False)
    truck_no = fields.Char('Truck/Vehicle No', size=100, readonly=True, states={'draft': [('readonly', False)]},
                           required=False)
    create_by = fields.Char('Carried By', size=100, readonly=True, states={'draft': [('readonly', False)]},
                            required=False)
    received = fields.Char('To Whom Received', size=100, readonly=True, states={'draft': [('readonly', False)]},
                           required=False)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.supplier_phone = self.partner_id.phone
