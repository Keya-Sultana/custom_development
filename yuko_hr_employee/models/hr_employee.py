from odoo import api, fields, models, _


_employee_type = [('trainee', 'Trainee'), ('permanent', 'Permanent'), ('parttime', 'Part time'), ('contractual', 'Contractual'),
                  ('fulltime', 'Full time'), ('intern', 'Intern'), ('consultant', 'Consultant'), ('provisional', 'Provisional')]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    birthday = fields.Date('Date of Birth', groups='base.group_user')
    employee_type = fields.Selection(_employee_type, string='Employee Type',)
    employee_pin = fields.Char('Employee PIN/Number', )
    employee_no = fields.Char('Employee ID NO', )
    employee_nid = fields.Char(string="National ID (NID)",)
    driving_licence = fields.Char('Driving Licence', )
    under_boss = fields.Char('Under/Reporting Boss', )
    # joining_date = fields.Date('Joining Date', )
    function = fields.Char('Function', )
    birth_certificate = fields.Char('Birth Certificate', )
    tin_no = fields.Char('TIN NO', )
    cell_phone = fields.Char('Cell Phone', )
    signature = fields.Char('Signature', )
    job_confirmation = fields.Date('Job Confirmation Date', )
    weight = fields.Char('Weight',)
    height = fields.Char('Height', )
    facebook = fields.Char('Facebook ID ', )
    designation = fields.Char('Designation')
    coach_id = fields.Many2one('hr.employee', string='Reporting Boss')
    employee_email = fields.Char('Email', )
    initial_employment_date = fields.Date( string='Joining Date',
        help='Date of first employment if it was before the start of the '
             'first contract in the system.',)


    #Emergency Contact
    emer_contact_name = fields.Char('Emergency Contact Name',)
    relation = fields.Char('Emergency Contact Relation')
    phone = fields.Char('Emergency Phone',)
    alt_phone = fields.Char('Emergency Alt. Phone')
    email = fields.Char('Emergency Email',)



    #Present Address information
    present_address = fields.Char('Present Address')
    present_thana = fields.Char('Present Thana')
    present_city = fields.Char('Present City')
    present_division = fields.Char('Present Division')
    present_postcode = fields.Char('Present Postcode')
    present_country = fields.Char('Country')

    #Permanent Address information
    permanent_address = fields.Char('Permanent Address')
    permanent_thana = fields.Char('Permanent Thana')
    permanent_po = fields.Char('Permanent Post Office')
    permanent_city = fields.Char('Permanent City')
    permanent_division = fields.Char('Permanent Division')
    permanent_postcode = fields.Char('Permanent Postcode')
    permanent_country = fields.Char('Country')

    # Official Contact Details
    user = fields.Char('User ID',)
    mail = fields.Char('Mail ID',)
    mobile_no = fields.Char('Mobile No',)
    social_network = fields.Char('Social Network ID',)




    
