from odoo import api, fields, models, _

class HrEmployeeTraining(models.Model):
    _name = 'hr.employee.training'
    

    training_name = fields.Char('Training Name',)
    start_date = fields.Date('Start Date',)
    end_date = fields.Date('End Date',)
    certification = fields.Char(string='Certification No', help='Certification Number')
    institution = fields.Char('Institution',)
    location = fields.Char('Location',)
    result = fields.Char('Result',)
    employee_id = fields.Many2one('hr.employee',
                                  string='Employee',
                                  required=True)


    
