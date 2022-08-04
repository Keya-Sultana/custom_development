from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'


    def _current_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True, select=True, invisible=False,track_visibility='onchange',default=_current_employee)

    manager_id = fields.Many2one('hr.employee', related='employee_id.parent_id', track_visibility='onchange',
                                 help='This area is automatically filled by the user who validate the exit process')

    state = fields.Selection(selection_add=[('department_managers', 'Department Managers '), ('audit', 'Audit'),
                                            ('management', 'Management'),('open', 'Open'), ('close', 'Closed')])

    # @api.multi
    # def action_paid(self):
    #     if self.due == 0.00:
    #         self.state = 'paid'
    #
    # @api.one
    # def check_pending_installment(self):
    #     for line in self:
    #         if line.due != '0.00':
    #             return False
    #     return True
    #
    # @api.multi
    # def action_reject(self):
    #     for record in self:
    #         record.state = 'reject'

    @api.multi
    def action_budget_confirm(self):
        super(CrossoveredBudget, self).action_budget_confirm()
        for iou in self:
            if iou.manager_id:
                self.message_post(body="You have been assigned to approve a Budget.",
                                  partner_ids=[iou.manager_id.sudo(SUPERUSER_ID).user_id.partner_id.id])



    @api.multi
    def action_approve_by_manager(self):

        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_employee_iou.group_audit')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="You have been assigned to approve a Budget.",
                                    partner_ids=partner_ids)
            record.state = 'department_managers'


    @api.multi
    def action_approve_by_audit(self):

        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_employee_iou.group_management')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="You have been assigned to approve a Budget.",
                                    partner_ids=partner_ids)
            record.state = 'audit'


    @api.multi
    def action_approve_by_management(self):

        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_employee_iou.group_account_adviser')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="You have been assigned to approve a Budget.",
                                    partner_ids=partner_ids)
            record.state = 'management'

    @api.multi
    def action_open(self):
        for record in self:
            record.state = 'open'

    @api.multi
    def action_close(self):
        today = fields.Date.from_string(fields.Date.today())
        end_date = fields.Date.from_string(self.date_to)
        if end_date > today:
            raise ValidationError(_("You can close after last date."))
        else:
            self.state = 'close'
