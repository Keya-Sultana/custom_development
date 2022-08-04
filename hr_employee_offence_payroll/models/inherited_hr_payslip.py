from odoo import api, fields, models, tools, _


class InheritedHrMobilePayslip(models.Model):
    """
    Inherit HR Payslip models and add onchange functionality on 
    employee_id
    """
    _inherit = "hr.payslip"

    remaining_loan = fields.Float(string='Remaining Loan', default=0.00, required=True)

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):

        if self.employee_id:

            emp_loan=self.env['hr.employee.offence'].search([('employee_id.id','=',self.employee_id.id),
                                                            ('state','=','valid')],limit=1)
            if emp_loan:
                self.remaining_loan = emp_loan.remaining_offence_amount or 0.00

            self.input_line_ids = 0
            super(InheritedHrMobilePayslip, self).onchange_employee()

            """
            Incorporate other payroll data
            """
            other_line_ids = self.input_line_ids
            loan_data = self.env['hr.employee.offence.line'].search([('employee_id', '=', self.employee_id.id),
                                                                  ('schedule_date', '>=', self.date_from),
                                                                  ('schedule_date', '<=', self.date_to),
                                                                  ('state', '=', 'pending')], limit=1)

            """
            Loan Amount
            """
            if loan_data and self.contract_id.id and loan_data.parent_id.state=='valid':
                other_line_ids += other_line_ids.new({
                    'name': 'Current Offence',
                    'code': "OFFENCE",
                    'amount': loan_data.installment,
                    'contract_id': self.contract_id.id,
                })
                self.input_line_ids = other_line_ids

    @api.multi
    def action_payslip_done(self):
        res = super(InheritedHrMobilePayslip, self).action_payslip_done()
        loan_data = self.env['hr.employee.offence.line'].search([('employee_id', '=', self.employee_id.id),
                                                              ('schedule_date', '>=', self.date_from),
                                                              ('schedule_date', '<=', self.date_to),
                                                              ('state', '=', 'pending')], limit=1)

        if loan_data and self.contract_id.id and loan_data.parent_id.state=='valid':
            loan_data.write({'state': 'done'})
            loan_data.parent_id.write({'remaining_offence_amount': loan_data.parent_id.remaining_offence_amount - loan_data.installment})

        return res


