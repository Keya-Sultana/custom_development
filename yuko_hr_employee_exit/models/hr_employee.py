from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    check_ids = fields.One2many('hr.exit.configure.checklists',
                                    'applicable_empname_id',
                                    'Checklists ID', readonly=True,
                                    help="Employee checklists ID")


    
