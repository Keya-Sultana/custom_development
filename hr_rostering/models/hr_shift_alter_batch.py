from odoo import models, fields,_,SUPERUSER_ID
from odoo import api
from odoo.exceptions import UserError, ValidationError

class HRShiftAlterBatch(models.Model):
    _name = 'hr.shift.alter.batch'
    _inherit = ['mail.thread']
    _description = 'HR Alter Roster Batch'

    name = fields.Char("Batch Name", required=True, readonly=True, copy=False, default='/')
    description = fields.Char(string='Description', required=False)
    shift_emp_ids = fields.Many2many('hr.employee', string="Employees",
                                     relation="hr_shift_alter_batch_rel",
                                     states={'confirmed': [('readonly', True)],
                                             'approved': [('readonly', True)],
                                             'refuse': [('readonly', True)]})

    alter_date = fields.Date(string='Alter Date', required=True)
    duty_start = fields.Datetime(string='Duty Start', required=True)
    duty_end = fields.Datetime(string='Duty End', required=True)
    is_included_ot = fields.Boolean(string='Is OT')
    ot_start = fields.Datetime(string='OT Start')
    ot_end = fields.Datetime(string='OT End')
    grace_time = fields.Float(string='Grace Time', default='1.5')

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('approved', "Approved"),
        ('refuse', 'Refused'),
    ], default='draft')

    def action_confirm(self):
        for record in self:
            if not record.shift_emp_ids:
                raise ValidationError(_('Please select at least one employee before confirming!!'))
            record.state = 'confirmed'

    def action_reject(self):
        for record in self:
            record.state = 'refuse'

    def action_approve(self):
        for record in self:
            for employee in record.shift_emp_ids:
                vals = {
                    'employee_id': employee.id,
                    'alter_date': record.alter_date,
                    'duty_start': record.duty_start,
                    'duty_end': record.duty_end,
                    'state': 'approved'
                }
                if record.is_included_ot:
                    vals['is_included_ot'] = True
                    vals['ot_start'] = record.ot_start
                    vals['ot_end'] = record.ot_end
                else:
                    vals['is_included_ot'] = False
                create_data = self.env['hr.shift.alter'].create(vals)
            record.write({'state': 'approved'})

    @api.model
    def create(self, vals):
        number = self.env['ir.sequence'].sudo().next_by_code('hr.shift.alter.batch') or '/'
        vals['name'] = number
        return super(HRShiftAlterBatch, self).create(vals)

