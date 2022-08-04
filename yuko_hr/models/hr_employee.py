from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def update_pf_amount(self):
        for emp in self:
            emp.total_pf = emp.init_pf + sum([float(line.amount) for line in emp.pf_lines]) or 0.00
