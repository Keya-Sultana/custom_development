from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class EmployeeOffenceType(models.Model):
    _name = 'employee.offence.type'
    _description = 'Employee Offence Type'

    name = fields.Char('Name', required=True, translate=True)