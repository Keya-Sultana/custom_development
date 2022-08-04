from odoo import api
from odoo import models, fields, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError


class HROTRequisition(models.Model):
    _name = 'hr.ot.requisition'
    _description = "HR OT Requisition"
    _inherit = ['mail.thread']
    _rec_name = 'employee_id'

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
                                  default=_default_employee, required=True, tracking=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department',
                                    readonly=True, store=True)
    from_datetime = fields.Datetime('Start Date', readonly=True, index=True, copy=False, required=True, tracking=True)
    to_datetime = fields.Datetime('End Date', readonly=True, copy=False, required=True, tracking=True)
    total_hours = fields.Float(string='Total hours', compute='_compute_total_hours', store=True, digits=(15, 2),
                               readonly=True, tracking=True)
    ot_reason = fields.Text(string='Reason for OT')
    user_id = fields.Many2one('res.users', string='User', related_sudo=True, store=True,
                              default=lambda self: self.env.uid, readonly=True)

    state = fields.Selection([
        ('to_submit', "To Submit"),
        ('to_approve', "To Approve"),
        ('approved', "Approved"),
        ('refuse', 'Refused'),
    ], default='to_submit', tracking=True)

    ####################################################
    # Business methods
    ####################################################

    @api.model
    def _notify_employee(self):
        for ot in self:
            if ot.sudo(SUPERUSER_ID).employee_id and \
                    ot.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your OT request has been Approved.",
                                  partner_ids=[ot.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.model
    def add_follower(self, employee_id):
        employee = self.env['hr.employee'].browse(employee_id)
        if employee.user_id:
            self.message_subscribe_users(user_ids=employee.user_id.ids)

    @api.constrains('from_datetime', 'to_datetime')
    def _check_to_datetime_validation(self):

        for ot in self:
            if ot.to_datetime < ot.from_datetime:
                raise ValidationError(_("End Time can not less then Start Time!!"))
        domain = [
            ('from_datetime', '<=', ot.to_datetime),
            ('to_datetime', '>=', ot.from_datetime),
            ('employee_id', '=', ot.employee_id.id),
            ('id', '!=', ot.id),
            ('state', 'not in', ['refuse']),
        ]
        domainOT = self.search_count(domain)
        if domainOT:
            raise ValidationError(_('You can not have multiple OT requisition on same day!'))

    @api.depends('from_datetime', 'to_datetime')
    def _compute_total_hours(self):
        if self.from_datetime and self.to_datetime:
            start_dt = fields.Datetime.from_string(self.from_datetime)
            finish_dt = fields.Datetime.from_string(self.to_datetime)
            diff = finish_dt - start_dt
            hours = float(diff.total_seconds() / 3600)
            self.total_hours = hours

    @api.constrains('total_hours')
    def _check_values(self):
        if self.total_hours == 0.0:
            raise ValidationError(_('Duration time should not be zero!!'))

    def action_submit(self):
        self.write({'state': 'to_approve'})

    def action_validate(self):
        for ot in self:
            ot.write({'state': 'approved'})
            ot._notify_employee()

    def action_refuse(self):
        self.write({'state': 'refuse'})

    def action_reset(self):
        self.write({'state': 'to_submit'})

    ####################################################
    # Override methods
    ####################################################

    @api.model
    def unlink(self):
        for a in self:
            if a.state != 'to_submit':
                raise UserError(_('You can not delete this.'))
            return super(HROTRequisition, self).unlink()

    # Showing batch
    @api.model
    def _needaction_domain_get(self):
        return [('state', 'in', ['to_approve'])]
