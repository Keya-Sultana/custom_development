from odoo import api
from odoo import models, fields,_,SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError


class HrShortLeave(models.Model):
    _inherit='hr.short.leave'

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="The status is set to 'To Submit', when a holiday request is created." +
             "\nThe status is 'To Approve', when holiday request is confirmed by user." +
             "\nThe status is 'Refused', when holiday request is refused by manager." +
             "\nThe status is 'Approved', when holiday request is approved by manager.")

    @api.multi
    def _compute_can_reset(self):
        """ User can reset a leave request if it is its own leave request or if he is an Hr Manager."""
        user = self.env.user
        #group_hr_manager = self.env.ref('hr_holidays.group_hr_holidays_user')
        for holiday in self:
            if holiday.employee_id and holiday.employee_id.user_id == user:
                holiday.can_reset = True


    @api.multi
    def _send_refuse_notification(self):
        for holiday in self:
                if holiday.sudo(SUPERUSER_ID).employee_id and \
                        holiday.sudo(SUPERUSER_ID).employee_id.user_id:
                    self.message_post(body="Your Short leave request has been refused.",
                                      partner_ids=[holiday.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.multi
    def action_refuse(self):
        self.write({'state': 'refuse', 'pending_approver': None})
        self._send_refuse_notification()

    @api.multi
    def action_confirm(self):
        super(HrShortLeave, self).action_confirm()
        for ot in self:
            if ot.employee_id.holidays_approvers:
                ot.pending_approver = ot.employee_id.holidays_approvers[0].approver.id
                self.message_post(body="You have been assigned to approve a Leave request.",
                                  partner_ids=[ot.pending_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def _notify_employee(self):
        for holiday in self:
            if holiday.sudo(SUPERUSER_ID).employee_id and \
                    holiday.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your Short leave request has been Approved.",
                                  partner_ids=[holiday.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

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

            self.env['hr.employee.short.leave.approbation'].create(
                {'short_leave_ids': ot.id, 'approver': self.env.uid, 'sequence': sequence,
                 'date': fields.Datetime.now()})

            if is_last_approbation:
                ot._notify_employee()
                ot.action_validate()
            else:
                vals = {'state': 'confirm'}
                if next_approver and next_approver.id:
                    vals['pending_approver'] = next_approver.id
                    if next_approver.sudo(SUPERUSER_ID).user_id:
                        self.suspend_security().message_post(
                            body="You have been assigned to approve a Leave request.",
                            partner_ids=[next_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])
                ot.suspend_security().write(vals)

    @api.multi
    def action_validate(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError('Only an Holidays Officer can Validate Leave request.')
        super(HrShortLeave, self).action_validate()
        for ot in self:
            ot.pending_approver = False
            ot._notify_employee()