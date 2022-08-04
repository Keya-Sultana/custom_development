from odoo import api
from odoo import models, fields,_,SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError


class HROTRequisition(models.Model):
    _inherit='hr.ot.requisition'

    @api.multi
    def action_submit(self):
        super(HROTRequisition, self).action_submit()
        for ot in self:
            if ot.employee_id.holidays_approvers:
                ot.pending_approver = ot.employee_id.holidays_approvers[0].approver.id
                self.message_post(body="You have been assigned to approve a OT Requisition.",
                                  partner_ids=[ot.pending_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def btn_action_approve(self):
        for ot in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            for approver in ot.employee_id.holidays_approvers:
                sequence = sequence + 1
                if ot.pending_approver.id == approver.approver.id:
                    if sequence == len(ot.employee_id.holidays_approvers):
                        is_last_approbation = True
                    else:
                        next_approver = ot.employee_id.sudo(SUPERUSER_ID).holidays_approvers[sequence].approver

            self.env['hr.employee.ot.approbation'].create(
                {'ot_ids': ot.id, 'approver': self.env.uid, 'sequence': sequence,
                 'date': fields.Datetime.now()})

            if is_last_approbation:
                ot.action_validate()
            else:
                vals = {'state': 'to_approve'}
                if next_approver and next_approver.id:
                    vals['pending_approver'] = next_approver.id
                    if next_approver.sudo(SUPERUSER_ID).user_id:
                        self.suspend_security().message_post(
                            body="You have been assigned to approve a OT Requisition.",
                            partner_ids=[next_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])
                ot.suspend_security().write(vals)

    @api.multi
    def action_validate(self):
        if not self.env.user.has_group('hr_attendance.group_hr_attendance_user'):
            raise UserError('Only an HR Officer can Validate OT Requisition.')
        super(HROTRequisition, self).action_validate()
        for ot in self:
            ot.pending_approver = False