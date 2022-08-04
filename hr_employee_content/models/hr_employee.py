from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    reference_ids = fields.One2many('hr.employee.reference',
                                   'employee_id',
                                   'Reference ID',
                                   help="Employee Reference ID")