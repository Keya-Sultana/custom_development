#-*- coding:utf-8 -*-

from odoo import models, fields

class EmployeeExitApprobation(models.Model):
    _name = "hr.employee.exit.approbation"
    _order= "sequence"
    
    exit_id = fields.Many2one('hr.emp.exit.req', string='Exit', required=True,ondelete="cascade",)
    approver_id = fields.Many2one('res.users', string='Approver', required=True,ondelete="cascade",)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
    