
from odoo import fields, api, models, _


class Contract(models.Model):
    _inherit = 'hr.contract'

    ot_wage = fields.Float(string='Overtime Rate/Hour')
    gross = fields.Float(string="Gross")
    job_respons = fields.Text(string="Job Responsibilities")
    holiday_allowance = fields.Float(string="Holidays Allowance")
    user_id = fields.Many2one('res.users', "Responsible",
                              default=lambda self: self.env.uid)
