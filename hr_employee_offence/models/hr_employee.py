from odoo import api, fields, models, _

class HrEmployeeNickName(models.Model):
    _inherit = 'hr.employee'

    offence_ids = fields.One2many('hr.employee.offence',
                                    'employee_id',
                                    'Offence ID', readonly=True,
                                    help="Employee Offence ID")


    
