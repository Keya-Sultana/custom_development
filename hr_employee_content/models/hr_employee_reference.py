from odoo import api, fields, models, _

class HrEmployeeReference(models.Model):
    _name = 'hr.employee.reference'
    

    name = fields.Char('Name',)
    organization = fields.Char('Organization',)
    designation = fields.Char('Designation',)
    relation = fields.Char('Relation',)
    phone_no = fields.Char('Phone No',)
    email_address = fields.Char('Email Address',)
    facebook_id = fields.Char('Facebook ID',)
    employee_id = fields.Many2one('hr.employee',
                                  string='Employee',
                                  required=True)


    
