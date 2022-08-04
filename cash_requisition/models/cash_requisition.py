from odoo import models, fields,_,SUPERUSER_ID
from odoo import api, fields, models
from odoo.osv import osv


class CashRequisition(models.Model):
    _name = 'cash.requisition'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _get_default_recorded_by(self):
        return self.env['res.users'].browse(self.env.uid)

    name = fields.Date(string='Date', required=True)
    requisition_by = fields.Many2one('res.users', string='Requisition By', required=True, track_visibility='onchange',
                                   default=_get_default_recorded_by)
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    line_ids = fields.One2many('cash.requisition.line', 'requisition_id', string="Cash Requisition Line",
                               required=False)
    note = fields.Text('Note', )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generate', 'Generated'),
        ('submit', 'Submitted'),
        ('approve', "Approved"),
    ], string="State", default='draft', track_visibility='onchange', )

    @api.depends('line_ids')
    def _compute_amount(self):
        for cash in self:
            #self.amount = sum([float(line.amount) for line in cash.line_ids]) or 0.00
            cash.amount = sum([l.amount for l in cash.line_ids if l.state == 'submit'])

    @api.one
    def action_generate(self):
        self.generate_lines()
        if self.state == 'draft':
            self.state = 'generate'

    @api.one
    def generate_lines(self):
        #self.ensure_one()
        lines = self.env['cash.requisition.line'].search([('name', '=', self.name), ('state', '=', 'submit')])
        lines.write({'requisition_id': self.id})

    @api.one
    def action_unlink(self):
        self.line_ids.write({'requisition_id': False})

    @api.one
    def action_submit(self):
        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_employee_iou.group_management')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="You have been assigned to approve a Daily Cash Requisition Summary.",
                                    partner_ids=partner_ids)
            record.state = 'submit'

    @api.one
    def action_approve(self):
        self.state = 'approve'

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'generate'):
                raise osv.except_osv(_('Warning!'), _('You cannot delete! It is in %s state.') % (rec.state))
        return super(CashRequisition, self).unlink()


class CashRequisitionLine(models.Model):
    _name = 'cash.requisition.line'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _get_default_recorded_by(self):
        return self.env['res.users'].browse(self.env.uid)

    name = fields.Date(string='Date', required=True)
    requisition_by = fields.Many2one('res.users', string='Requisition By', required=True, track_visibility='onchange',
                                   default=_get_default_recorded_by)
    amount = fields.Float(string='Amount')
    requisition_id = fields.Many2one('cash.requisition', string="Cash Requisition")
    note = fields.Char('Note',size=100)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
    ], string="State", default='draft', track_visibility='onchange', )

    @api.one
    def action_submit(self):
        for record in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_employee_iou.group_account_adviser')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                record.message_post(body="Daily Cash Requisition is submitted.",
                                    partner_ids=partner_ids)
            record.state = 'submit'

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise osv.except_osv(_('Warning!'), _('You cannot delete! It is in %s state.') % (rec.state))
        return super(CashRequisitionLine, self).unlink()




