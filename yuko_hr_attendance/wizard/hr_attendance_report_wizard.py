from openerp import models, fields, api


class EmpAttendanceReportWizard(models.TransientModel):
    _name = 'employee.attendance.report.wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee',)
