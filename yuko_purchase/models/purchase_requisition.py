from odoo import _
from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    state = fields.Selection([('draft', 'Draft'), ('progress', 'Confirmed'),
                              ('approve_procurement', 'Waiting For Approval'), ('done', 'Approved'),
                              ('close', 'Done'),
                              ('cancel', 'Cancelled')], 'Status', track_visibility='onchange', required=True,
                             copy=False, default='draft')

    @api.multi
    def action_in_progress(self):
        for pr in self:
            if not pr.line_ids:
                raise UserError(_('You cannot confirm, because there is no product line.'))

            res = {'state': 'progress'}

            requested_date = self.requisition_date
            operating_unit = self.operating_unit_id
            new_seq = self.env['ir.sequence'].next_by_code_new('purchase.requisition', requested_date, operating_unit)

            if new_seq:
                res['name'] = new_seq

            pr.write(res)

            # Send Notification
            partner_ids = []
            grp = self.env.ref('gbs_purchase_requisition.group_purchase_requisition_approver')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                pr.message_post(body="You have been assigned to approve.",
                                partner_ids=partner_ids)

    @api.multi
    def action_done(self):
        """
        Generate all purchase order based on selected lines, should only be called on one agreement at a time
        """
        if any(purchase_order.state in ['draft', 'sent', 'to approve'] for purchase_order in
               self.mapped('purchase_ids')):
            raise UserError(_('You have to cancel or validate every RfQ before closing the purchase requisition.'))
        self.write({'state': 'close'})


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    date = fields.Date('Date')
