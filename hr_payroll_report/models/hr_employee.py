from openerp import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    loan_id = fields.Many2one('hr.employee.loan', string='Employee Loan',
                                      help='Employee Loan Request', groups='hr.group_hr_user')


