from openerp import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def amount_to_text(self, total_amount):
        amt_to_word = self.env['res.currency'].amount_to_word(total_amount)
        return amt_to_word

    @api.depends('line_ids.total')
    def _amount_all(self):
        """
        Compute the total amounts of the Payslip line.
        """
        for payslip in self:
            total_amount = 0.0
            for line in payslip.line_ids:
                total_amount += line.total
            payslip.update({
                'total_amount': total_amount,
            })

    total_amount = fields.Float(compute='_amount_all', store=True, readonly=True,
                                string='Total Payable Amount', track_visibility='always')


class ProvidentFundWizard(models.TransientModel):
    _inherit = "provident.fund.wizard"

    @api.depends('employee_id')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if not res_user.has_group('hr.group_hr_user') and not res_user.has_group('hr.group_hr_manager'):
            self.compute_field = False
        else:
            self.compute_field = True


class HrPayslipRun(models.Model):
    _name = 'hr.payslip.run'
    _inherit = ['hr.payslip.run', 'mail.thread']

    run = fields.Char(string='Run')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('close', 'Close'),
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft')

    @api.multi
    def _track_subtype(self, init_values):
        if 'state' in init_values and self.state == 'close':
            return 'hr_payroll_report.mt_payslip_close'
        return super(HrPayslipRun, self)._track_subtype(init_values)