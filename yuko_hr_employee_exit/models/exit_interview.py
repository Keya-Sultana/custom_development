# -*- coding:utf-8 -*-

from odoo import fields, models, api, _
import datetime
from datetime import timedelta
from odoo import models, fields, api, SUPERUSER_ID

class EmployeeEixtInterview(models.Model):
    _inherit = 'employee.exit.interview'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('validate', 'Supervisor Approved'),
        ('approved', ' HR Director Approved'),
    ], string='Status', default='draft', track_visibility='onchange')

    @api.multi
    def action_submit(self):
        super(EmployeeEixtInterview, self).action_submit()
        for exit in self:
            if exit.supervisor_id:
                self.message_post(body="You have been assigned to approve a Exit Interview.",
                                  partner_ids=[exit.supervisor_id.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def action_emp_notify(self):
        for exit in self:
            if exit.employee_id:
                self.message_post(body="You are selected for Exit Interview.",
                                  partner_ids=[exit.employee_id.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.model
    def send_email_notification(self):

        su_id = self.env['res.partner'].browse(SUPERUSER_ID)
        template_id = self.env['ir.model.data'].get_object_reference('yuko_hr_employee_exit',
                                                                     'email_notification_template_exit')[1]
        template_browse = self.env['mail.template'].browse(template_id)

        if template_browse:
            grp = self.env['res.groups'].search([('full_name', '=', "Employees/HR Director ")], limit=1)
            for user in grp.users:
                values = template_browse.generate_email(user.id, fields=None)
                values['subject'] = values['subject'] + " " + str(datetime.date.today())
                values['email_to'] = user.email
                values['email_from'] = su_id.email
                values['res_id'] = False
                if not values['email_to'] and not values['email_from']:
                    pass
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.create(values)
                if msg_id:
                    mail_mail_obj.send(msg_id)

    @api.multi
    def action_validate(self):
        super(EmployeeEixtInterview, self).action_validate()
        self.send_email_notification()


