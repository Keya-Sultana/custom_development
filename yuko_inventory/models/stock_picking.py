# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Picking(models.Model):
    _inherit = "stock.picking"

    gate_in_no = fields.Char(
        string='Gate In No',
        readonly=True,
        states={'draft': [('readonly', False)], 'assigned': [('readonly', False)]})



    @api.multi
    @api.depends('receive_type', 'location_dest_id', 'check_mrr_button', 'state')
    def _compute_approve_button(self):
        for picking in self:
            if picking.state == 'done' and picking.location_dest_id.name == 'Stock':
                # Search from anticipatory stock
                if picking.check_mrr_button:
                    #picking.check_ac_approve_button = False
                    picking.check_approve_button = False
                else:
                    # Search from anticipatory stock
                    origin_picking_objs = self.search(
                        ['|', ('name', '=', picking.origin), ('origin', '=', picking.origin)],
                        order='id ASC', limit=1)
                    # if anticipatory then conditionally search that its type
                    if origin_picking_objs:
                        if origin_picking_objs.receive_type == 'loan':
                            #picking.check_ac_approve_button = False
                            picking.check_approve_button = False
                        else:
                            #picking.check_ac_approve_button = True
                            picking.check_approve_button = True
                    else:
                        #picking.check_ac_approve_button = True
                        picking.check_approve_button = True