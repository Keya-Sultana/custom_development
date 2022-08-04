import datetime

from dateutil.relativedelta import relativedelta
from odoo import api
from odoo import models, fields,_,SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError



class HrEmployeeOffence(models.Model):
    _name = 'hr.employee.offence'
    _inherit = ['mail.thread', 'ir.needaction_mixin']


    @api.model
    def _get_default_recorded_by(self):
        return self.env['res.users'].browse(self.env.uid)

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    offence_ids = fields.One2many('hr.employee.offence',
                                  'employee_id',
                                  'Offence ID', readonly=True,
                                  help="Employee Offence ID")

    name = fields.Char(string='Reference Number')
    offence_date = fields.Date('Offence Date', )
    offence_type = fields.Many2one('employee.offence.type', required=True,
                                   string= "Offence Type")
    recorded_by = fields.Many2one('res.users', string= 'Recorded By',
                                   required=True,
                                   track_visibility='onchange',
                                   default=_get_default_recorded_by)
    partner_id = fields.Many2one(
        'res.partner', string='Partner',
        default=lambda self: self.env.user.company_id.partner_id)
    description=fields.Text(string="Description", )
    replies = fields.Text(string="Employee's Replies", )
    damaged_amount = fields.Float(string="Damaged Amount", )
    penalty_amount = fields.Float(string="Penalty Amount", )
    offence_category = fields.Selection([('major', 'Major'), ('minor', 'Minor'), ('termination', 'Termination')], 'Offence Category', default='major')

    installment_amount = fields.Integer(size=100, string='Installment Amount',
                                        states={'draft': [('readonly', True)], 'confirm': [('readonly', False)],
                                                'valid': [('readonly', True)], 'feedback': [('readonly', True)],
                                                'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    remaining_offence_amount = fields.Float(string="Remaining Amount", digits=(15, 2), readonly=True,
                                         states={'draft': [('invisible', True)], 'confirm': [('invisible', True)],
                                                 'feedback': [('invisible', False)],'done': [('invisible', False)],
                                                 'valid': [('invisible', False)]})
    repayment_date = fields.Date('Repayment Date',
                                 states={'draft': [('readonly', True)], 'confirm': [('readonly', False)],
                                         'valid': [('readonly', True)], 'feedback': [('readonly', True)],
                                         'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    line_ids = fields.One2many('hr.employee.offence.line', 'parent_id', string="Employee offence Installment Schedule",
                               states={'draft': [('invisible', False)], 'confirm': [('readonly', True)],
                                       'valid': [('readonly', True)], 'feedback': [('readonly', True)],
                                       'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('valid', 'Validate'),
        ('feedback', 'Feedback'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string="State", default='draft', track_visibility='onchange',)

    employee_id = fields.Many2one('hr.employee',
                                  string='Employee Name',
                                  required=True, default=_default_employee)

    @api.multi
    def generate_schedules(self):
        for loan in self:
            if loan.installment_amount > 0 and loan.repayment_date and len(loan.line_ids) == 0:
                repayment_date = datetime.datetime.strptime(loan.repayment_date, '%Y-%m-%d')
                # installment = loan.principal_amount / int(loan.installment_amount)
                loan.line_ids.unlink()
                p_amount = loan.penalty_amount
                i = 1
                while p_amount > 0:
                    vals = {}
                    vals['employee_id'] = loan.employee_id.id
                    vals['schedule_date'] = repayment_date
                    if p_amount > loan.installment_amount:
                        vals['installment'] = loan.installment_amount
                    else:
                        vals['installment'] = p_amount
                    vals['num_installment'] = i
                    vals['parent_id'] = loan.id
                    repayment_date = repayment_date + relativedelta(months=1)
                    loan.line_ids.create(vals)
                    i += 1
                    p_amount -= loan.installment_amount


    # Auto generate reference number

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.offence')
        return super(HrEmployeeOffence, self).create(vals)

    @api.multi
    def _send_refuse_notification(self):
        for offence in self:
            if offence.sudo(SUPERUSER_ID).employee_id and \
                    offence.sudo(SUPERUSER_ID).employee_id.user_id:
                self.message_post(body="Your Offence request has been refused.",
                                  partner_ids=[offence.sudo(SUPERUSER_ID).employee_id.user_id.partner_id.id])

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    def action_cancel(self):
        self.write({'state': 'cancel', 'pending_approver': None})
        self._send_refuse_notification()

    @api.one
    def action_confirm(self):
        self.state = 'confirm'


    @api.one
    def action_valid(self):
        self.state = 'valid'
        self.remaining_offence_amount = self.penalty_amount

    @api.one
    def action_feedback(self):
        self.state = 'feedback'

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise osv.except_osv(_('Warning!'), _('You cannot delete! It is in %s state.') % (rec.state))
        return super(HrEmployeeOffence, self).unlink()

    def action_recorded(self, cr, uid, ids, context=None):
        vals = {
            'state':'draft',
            'recorded_by': uid,
        }
        return self.write(cr, uid, ids, vals)

    @api.multi
    def action_send_amc(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('hr_employee_offence', 'email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'hr.employee.offence',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
