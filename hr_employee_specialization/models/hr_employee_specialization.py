from odoo import api, fields, models, _

class HrEmployeeSpecialization(models.Model):
    _name = 'hr.employee.specialization'
    

    type = fields.Char('Type',)
    item = fields.Char('Item',)
    category = fields.Char('Category',)
    priority = fields.Char('Priority',)
    performance = fields.Char('Performance',)
    productivity = fields.Char('Productivity',)
    comments = fields.Char('Comments',)

    employee_id = fields.Many2one('hr.employee',
                                  string='Employee',
                                  required=True)


    
