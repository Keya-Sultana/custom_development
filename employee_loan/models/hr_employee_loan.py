from odoo import api, fields, models


class HrEmployeeLoanPolicy(models.Model):
    _inherit = 'hr.employee.loan.policy'

    eligibility = fields.Text('General Eligibility',)
    basis_id = fields.Selection(selection_add=[('percent_wage', 'Percent of Wage')])


class HrEmployeeLoan(models.Model):
    _inherit = 'hr.employee.loan'



    guarantor_emp = fields.Char(string="Guarantor Employee",
                                  states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})

    guarantor_name = fields.Char('Guarantor Name', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    date_of_birth = fields.Date('Date of birth', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    guarantor_nid = fields.Char('Guarantor NID', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    photo = fields.Binary('Photo', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    father_name = fields.Char('Father Name', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    mother_name = fields.Char('Mother Name', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    address = fields.Char('Address', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    contact = fields.Char('Contact Info', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})
    signature = fields.Binary('Signature', states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})


    is_employee = fields.Boolean(string='Is a Employee', default=False,
                                help="Check if the contact is a Employee, otherwise it is a Non Employee")
    guarantor_type = fields.Selection(string='Guarantor Type :',
                                selection=[('non_employee', 'Non Employee'), ('employee', 'Employee')],
                              compute='_compute_guarantor_type', inverse='_write_guarantor_type',
                                states={'draft': [('invisible', False)], 'applied': [('readonly', True)], 'approved':[('readonly', True)],'disbursed':[('readonly', True)]})

    @api.depends('is_employee')
    def _compute_guarantor_type(self):
        for partner in self:
            partner.guarantor_type = 'employee' if partner.is_employee else 'non_employee'

    def _write_guarantor_type(self):
        for partner in self:
            partner.is_employee = partner.guarantor_type == 'employee'

    @api.onchange('guarantor_type')
    def onchange_guarantor_type(self):
        self.is_employee = (self.guarantor_type == 'employee')

    @api.multi
    def action_close(self):
        for loan in self:
            if loan.state == 'disbursed' and loan.check_pending_installment()[0]:
                loan.write({'state': 'closed'})
