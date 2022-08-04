#-*- coding:utf-8 -*-

from odoo import models, fields

class MaternityHolidayApprobation(models.Model):
    _name = "hr.maternity.holiday.approbation"
    _order= "sequence"
    
    maternity_id = fields.Many2one('hr.maternity.holiday', string='Maternity', required=True,ondelete="cascade",)
    approver_id = fields.Many2one('res.users', string='Approver', required=True,ondelete="cascade",)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
    