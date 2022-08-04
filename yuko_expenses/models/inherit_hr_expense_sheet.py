from odoo import api, fields, models, tools, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    state = fields.Selection([('draft', "Draft"),
                              ('submit', 'Submitted'),
                              ('approve', 'Approved'),
                              ('post', 'Posted'),
                              ('done', 'Paid'),
                              ('cancel', 'Refused')
                              ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False,
                             default='draft', required=True,
                             help='Expense Report State')

    @api.one
    def action_confirm(self):
        self.state = 'submit'