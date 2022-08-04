from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PRFromWhereWizard(models.TransientModel):
    _name = 'pr.from.where.wizard'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    purchase_from = fields.Selection([('ho', 'HO')], string="Purchase From")

    # today
    region_type = fields.Selection([('local', 'Local'), ('foreign', 'Foreign')], string="Region Type")

    purchase_by = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ('lc', 'LC'), ('tt', 'TT')],
                                   string="Purchase By")
    name = fields.Char("Name")

    @api.multi
    def save_type(self):
        for pr in self:
            # validation
            if pr.region_type == 'local' and pr.purchase_by == 'tt':
                raise UserError(_("Invalid Input" + "\nFor Foreign Purchase: Apply LC or TT. " + "\nLocal Purchase: Apply Cash, Credit or LC."))

            elif pr.region_type == 'foreign' and (pr.purchase_by == 'cash' or pr.purchase_by == 'credit'):
                raise UserError(_("Invalid Input" + "\nFor Foreign Purchase: Apply LC or TT. " + "\nLocal Purchase: Apply Cash, Credit or LC."))

            form_id = pr.env.context.get('active_id')
            pr_form_pool = pr.env['purchase.requisition'].search([('id', '=', form_id)])
            pr.name = pr_form_pool.name
            # check purchase from
            if pr.purchase_from == 'own':
                pr_form_pool.write({'purchase_from': pr.purchase_from, 'region_type': pr.region_type,
                                    'purchase_by': pr.purchase_by, 'state': 'done'})
            else:
                pr_form_pool.write({'purchase_from': pr.purchase_from, 'region_type': pr.region_type,
                                    'purchase_by': pr.purchase_by, 'state': 'approve_procurement'})
            # get the purchase order for this requisition
            po_pool_obj = pr.env['purchase.order'].search([('requisition_id', '=', form_id)])
            if po_pool_obj:
                po_pool_obj.write({'check_po_action_button': True,
                                   'region_type': pr.region_type or False,
                                   'purchase_by': pr.purchase_by or False})

            #if pr.name:



                # Send Notification
            partner_ids = []
            grp = self.env.ref('gbs_purchase_requisition.group_purchase_requisition_validator')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                pr.message_post(body="You have been assigned to validate.",
                                partner_ids=partner_ids)

            return {'type': 'ir.actions.act_window_close'}

    # @api.multi
    # def cancel_window(self):
    #     form_id = self.env.context.get('active_id')
    #     pr_form_pool = self.env['purchase.requisition'].search([('id', '=', form_id)])
    #     pr_form_pool.write({'state': 'done'})
    #     po_pool_obj = self.env['purchase.order'].search([('requisition_id', '=', form_id)])
    #     if po_pool_obj:
    #         po_pool_obj.write({'check_po_action_button': True})
    #     return {'type': 'ir.actions.act_window_close'}










