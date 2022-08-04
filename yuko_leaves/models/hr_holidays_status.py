from odoo import api, fields, tools, models, _



class HRHolidayStatus(models.Model):
    _inherit = 'hr.holidays.status'

    terms_condition = fields.Text(string='Terms of Condition')