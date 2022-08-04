#-*- coding:utf-8 -*-

from odoo import models, fields

class EmployeeOffenceApprobation(models.Model):
    _name = "hr.employee.offence.approbation"
    _order= "sequence"
    
    offence_id = fields.Many2one('hr.employee.offence', string='Offence', required=True,ondelete="cascade",)
    approver_id = fields.Many2one('res.users', string='Approver', required=True,ondelete="cascade",)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
    