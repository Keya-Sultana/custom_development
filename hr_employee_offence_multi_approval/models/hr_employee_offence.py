#-*- coding:utf-8 -*-
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _

class Offence(models.Model):
    _name = 'hr.employee.offence'
    _inherit = ['hr.employee.offence','mail.thread']

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



    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", readonly=True, default=_default_approver)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user', related='pending_approver.user_id', related_sudo=True, store=True, readonly=True)
    current_user_is_approver = fields.Boolean(string= 'Current user is approver', compute='_compute_current_user_is_approver')
    approbations = fields.One2many('hr.employee.offence.approbation', 'offence_id', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user',compute="_compute_pending_transfered_approver_user", search='_search_pending_transfered_approver_user')


    @api.model
    def create(self, values):
        if values.get('employee_id', False):
            employee = self.env['hr.employee'].browse(values['employee_id'])
            if employee and employee.holidays_approvers and employee.holidays_approvers[0]:
                values['pending_approver'] = employee.holidays_approvers[0].approver.id
        res = super(Offence, self).create(values)
        return res



    @api.multi
    def action_confirm(self):
        super(Offence, self).action_confirm()
        for offence in self:
            if offence.employee_id.holidays_approvers:
                offence.pending_approver = offence.employee_id.holidays_approvers[0].approver.id
                self.message_post(body="You have been assigned to approve a Offence.", partner_ids=[offence.pending_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def _notify_employee(self):
        for offence in self:
            if offence.sudo(SUPERUSER_ID).employee_id and \
                    offence.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your Offence request has been Approved.",
                                  partner_ids=[offence.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.multi
    def btn_action_approve(self):
        for offence in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            for approver in offence.employee_id.holidays_approvers:
                sequence = sequence + 1
                if offence.pending_approver.id == approver.approver.id:
                    if sequence == len(offence.employee_id.holidays_approvers):
                        is_last_approbation = True
                    else:
                        next_approver = offence.employee_id.sudo(SUPERUSER_ID).holidays_approvers[sequence].approver

            self.env['hr.employee.offence.approbation'].create(
                {'offence_id': offence.id, 'approver_id': self.env.uid, 'sequence': sequence,
                 'date': fields.Datetime.now()})

            if is_last_approbation:
                offence._notify_employee()
                offence.action_validate()
            else:
                vals = {'state': 'confirm'}
                if next_approver and next_approver.id:
                    vals['pending_approver'] = next_approver.id
                    if next_approver.sudo(SUPERUSER_ID).user_id:
                        self.suspend_security().message_post(body="You have been assigned to approve a Offence.",
                                          partner_ids=[next_approver.sudo(SUPERUSER_ID).user_id.partner_id.id])
                offence.suspend_security().write(vals)

    @api.multi
    def action_validate(self):
        if not self.env.user.has_group('hr.group_hr_manager'):
            raise UserError('Only an HR Manager can Validate Employee Offence.')
        super(Offence, self).action_valid()
        for requisition in self:
            requisition.pending_approver = False
            requisition._notify_employee()

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

