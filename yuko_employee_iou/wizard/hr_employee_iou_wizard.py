from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError


class HrEmployeeIouWizard(models.TransientModel):
    _inherit = 'hr.employee.iou.wizard'

    @api.multi
    def process_repayment(self):

        emp_iou_pool = self.env['hr.employee.iou'].browse([self._context['active_id']])

        amount = emp_iou_pool.amount
        due_amount = emp_iou_pool.due
        emp_id = emp_iou_pool.employee_id.id
        state = emp_iou_pool.state

        if self.repay is not None and amount is not None:
            if (self.repay > amount or self.repay > due_amount):
                raise UserError(('Repayment can not be greater than actual amount'))

        if self.repay:
            self.env['hr.employee.iou.line'].create({
                'iou_id': self._context['active_id'],
                'repay_amount': self.repay, 'employee_id': emp_id
            })

        if self.repay < 0 :
            raise UserError(('Repayment can not be Negative amount'))

        due = due_amount - self.repay
        if due == 0.00:
            emp_iou_pool.write({'state': 'paid'})


        # for line_state in emp_iou_pool:
        #     if line_state.state == 'confirm':
        #         values = {}
        #         if line_state.check_pending_installment() == False:
        #             values['state'] = 'paid'
        #
        #         line_state.write(values)




    # @api.multi
    # def process_repayment(self):
    #     super(HrEmployeeIouWizard, self).process_repayment()
    #
    #     loan_data = self.env['hr.employee.iou'].browse([self._context['active_id']])
    #
    #     for line_state in loan_data:
    #         if line_state.state == 'disbursed':
    #             values = {}
    #             if line_state.check_pending_installment() == True:
    #                 values['state'] = 'paid'
    #
    #             line_state.write(values)
    #
    #     # for line_state in emp_iou_pool:
    #     #     if line_state.due == '0.00':
    #     #         line_state.write({'state': 'paid'})
    #
    #     # for iou in self.iou_ids:
    #     #     iou.action_paid()





