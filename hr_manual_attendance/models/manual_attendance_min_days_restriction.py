from odoo import api
from odoo import fields
from odoo import models


class HrManualAttendanceMinDaysRestriction(models.Model):
    _inherit = 'res.config.settings'
    _name = 'hr.manual.attendance.min.days'
    _description = 'Hr Manual Attendance Min Days Restriction'
    
    min_days_restriction = fields.Integer(string='Minimum Days Restriction', default=30)
    