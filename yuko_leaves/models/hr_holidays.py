from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError



class HRHolidays(models.Model):
    _inherit = 'hr.holidays'


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    #handover_employee = fields.Many2one('hr.employee', string='Duty Handover Employee')
    name = fields.Text('Description')
    duty_handover = fields.Char(string='Duty Handover Employee', readonly=True, states={'draft': [('readonly', False)]})
    holiday_status_id = fields.Many2one("hr.holidays.status", string="Leave Type", required=True, readonly=True,
                                        states={'draft': [('readonly', False)]})
    date_from = fields.Date('Start Date', readonly=True, index=True, copy=False,
                                states={'draft': [('readonly', False)]})
    date_to = fields.Date('End Date', readonly=True, copy=False,
                              states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  default=_default_employee)

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
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
        # group_hr_manager = self.env.ref('hr_holidays.group_hr_holidays_user')
        for holiday in self:
            if holiday.employee_id and holiday.employee_id.user_id == user:
                holiday.can_reset = True

    #def _check_state_access_right(self, vals):
    #    if vals.get('state') and vals['state'] not in ['draft', 'confirm', 'cancel'] and not self.env['res.users'].has_group('hr_holidays.group_hr_holidays_user'):
     #       return False
     #   return True

    @api.multi
    def action_reset_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def action_confirm(self):
        super(HRHolidays, self).action_confirm()
        for holiday in self:
            if holiday.employee_id.holidays_approvers:
                holiday.pending_approver = holiday.employee_id.holidays_approvers[0].approver.id
                self.message_post(body="You have been assigned to approve a Leave Request.",
                                  partner_ids=[holiday.pending_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])

