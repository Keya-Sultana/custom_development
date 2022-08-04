# -*- coding:utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError


class EmployeeExitReq(models.Model):
    _inherit = 'hr.emp.exit.req'


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    @api.multi
    def _default_approver(self):
        default_approver = 0
        employee = self._default_employee()
        if isinstance(employee, int):
            emp_obj = self.env['hr.employee'].search([('id', '=', employee)], limit=1)
            if emp_obj.sudo().holidays_approvers:
                default_approver = emp_obj.sudo().holidays_approvers[0].approver.id
        else:
            if employee.sudo().holidays_approvers:
                default_approver = employee.sudo().holidays_approvers[0].approver.id
        return default_approver


    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", readonly=True,
                                       default=_default_approver)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user',
                                            related='pending_approver.user_id', related_sudo=True, store=True,
                                            readonly=True)
    current_user_is_approver = fields.Boolean(string='Current user is approver',
                                              compute='_compute_current_user_is_approver')
    approbations = fields.One2many('hr.employee.exit.approbation', 'exit_id', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user',
                                                       compute="_compute_pending_transfered_approver_user",
                                                       search='_search_pending_transfered_approver_user')
    can_reset = fields.Boolean('Can reset', compute='_compute_can_reset')

    state = fields.Selection(
        [('draft', 'To Submit'),
         ('cancel', 'Cancelled'),
         ('confirm', 'To Approve'),
         ('refuse', 'Refused'),
         ('validate', 'Approved')],
        'Status', readonly=True, copy=False, default='draft',
        help='The status is set to \'To Submit\', when a Exit request is created.\
                \nThe status is \'To Approve\', when exit request is confirmed by user.\
                \nThe status is \'Refused\', when exit request is refused by manager.\
                \nThe status is \'Approved\', when exit request is approved by manager.', track_visibility='onchange')

    @api.multi
    def action_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def action_confirm(self):
        super(EmployeeExitReq, self).exit_confirm()
        for exit in self:
            if exit.employee_id.holidays_approvers:
                exit.pending_approver = exit.employee_id.holidays_approvers[0].approver.id
                self.message_post(body="You have been assigned to approve a Exit Request.",
                                  partner_ids=[exit.pending_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def _notify_employee(self):
        for exit in self:
            if exit.sudo(SUPERUSER_ID).employee_id and \
                    exit.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your Exit Request has been Approved.",
                                  partner_ids=[exit.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.multi
    def _compute_can_reset(self):
        """ User can reset a leave request if it is its own leave request or if he is an Hr Manager."""
        user = self.env.user
        # group_hr_manager = self.env.ref('hr_holidays.group_hr_holidays_user')
        for holiday in self:
            if holiday.employee_id and holiday.employee_id.user_id == user:
                holiday.can_reset = True

    @api.multi
    def btn_action_approve(self):
        for exit in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            for approver in exit.employee_id.holidays_approvers:
                sequence = sequence + 1
                if exit.pending_approver.id == approver.approver.id:
                    if sequence == len(exit.employee_id.holidays_approvers):
                        is_last_approbation = True
                    else:
                        next_approver = exit.employee_id.sudo(SUPERUSER_ID).holidays_approvers[sequence].approver

            self.env['hr.employee.exit.approbation'].create(
                {'exit_id': exit.id, 'approver_id': self.env.uid, 'sequence': sequence,
                 'date': fields.Datetime.now()})

            if is_last_approbation:
                exit._notify_employee()
                exit.action_validate()
            else:
                vals = {'state': 'confirm'}
                if next_approver and next_approver.id:
                    vals['pending_approver'] = next_approver.id
                    if next_approver.sudo(SUPERUSER_ID).user_id:
                        self.suspend_security().message_post(body="You have been assigned to approve a Exit Request.",
                                                             partner_ids=[next_approver.sudo(
                                                                 SUPERUSER_ID).user_id.partner_id.id])
                exit.suspend_security().write(vals)

    @api.multi
    def action_validate(self):
        if not self.env.user.has_group('hr.group_hr_manager'):
            raise UserError('Only an HR Manager can Validate Employee Exit Request.')
        super(EmployeeExitReq, self).exit_done()
        for request in self:
            request.pending_approver = False
            self.write({'state': 'validate'})
            self._notify_employee()

    @api.multi
    def _send_refuse_notification(self):
        for holiday in self:
            if holiday.sudo(SUPERUSER_ID).employee_id and \
                    holiday.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your Exit request has been refused.",
                                  partner_ids=[holiday.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.multi
    def exit_refuse(self):
        super(EmployeeExitReq, self).exit_refuse()
        self._send_refuse_notification()


    @api.one
    def _compute_current_user_is_approver(self):
        if self.pending_approver.user_id.id == self.env.user.id or self.pending_approver.transfer_holidays_approvals_to_user.id == self.env.user.id:
            self.current_user_is_approver = True
        else:
            self.current_user_is_approver = False

    @api.one
    def _compute_pending_transfered_approver_user(self):
        self.pending_transfered_approver_user = self.pending_approver.transfer_holidays_approvals_to_user

    def _search_pending_transfered_approver_user(self, operator, value):
        replaced_employees = self.env['hr.employee'].search([('transfer_holidays_approvals_to_user', operator, value)])
        employees_ids = []
        for employee in replaced_employees:
            employees_ids.append(employee.id)
        return [('pending_approver', 'in', employees_ids)]
