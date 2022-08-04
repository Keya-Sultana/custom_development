# -*- coding:utf-8 -*-

from odoo import fields, models, api, _

class FinalSettlement(models.Model):
    _inherit = 'final.settlement'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', ' HR Director Approved'),
    ], string='Status', default='draft', track_visibility='onchange')

    @api.multi
    def action_confirm(self):
        vals = []
        epm_slip = self.env['hr.payslip'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'validate')], order='date_to DESC', limit=1)
        for fac in epm_slip.line_ids:
            if fac.code in ('BASIC', 'TCA', 'OAS', 'MEDA', 'HRAMN', 'GROSS'):
                vals.append((0, 0, {
                    'code': fac.code,
                    'name': fac.name,
                    'total': fac.total,
                }))
        self.emp_payslip_ids = vals
        self.state = 'confirm'
        #self.payment_ids.write({'state': 'confirm'})
        #self.deduction_ids.write({'state': 'confirm'})
        #self.emp_payslip_ids.write({'state': 'confirm'})


