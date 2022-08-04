from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    speciali_ids = fields.One2many('hr.employee.specialization',
                                   'employee_id',
                                   'Specialization Information',
                                   help="Specialization Information")