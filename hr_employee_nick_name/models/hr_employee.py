from odoo import api, fields, models, _

class HrEmployeeNickName(models.Model):
    _inherit = 'hr.employee'
    

    employee_nickname = fields.Char('Employee Nick Name',)
    #identification_id = fields.Char(string='Official Id', groups='hr.group_hr_user')


    
