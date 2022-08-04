from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    training_ids = fields.One2many('hr.employee.training',
                                   'employee_id',
                                   'Training',
                                   help="Training")