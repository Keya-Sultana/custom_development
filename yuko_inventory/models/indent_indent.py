from odoo import models, fields, api, SUPERUSER_ID


class IndentIndent(models.Model):
    _inherit = 'indent.indent'


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True,
                              compute_sudo=True, store=True, default=lambda self: self.env.uid, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Indenter', index=True, readonly=True,
                                  default=_default_employee)
    depart_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Indenter Department',
                                    readonly=True, store=True)
    indenter_no = fields.Char("Indenter Employee ID", readonly=True, store=True)

    state = fields.Selection(selection_add=[('cancel', 'Cancel')])

    rejection_reason =fields.Text("Rejection Reason")

    indent_type = fields.Many2one('indent.type',string='Type',readonly=True, required = False, states={'draft': [('readonly', False)]})


    #department_id = fields.Many2one('stock.location', string='Department',)
    #stock_location_id = fields.Many2one('stock.location', string='Department', readonly=True, required=False,
    #                                    states={'draft': [('readonly', False)]},
    #                                    help="Default User Location.Which consider as Destination location.",
    #                                    default=lambda self: self.env.user.default_location_id)

    #stockl_id = fields.Many2one('stock.location', string='Department', required=True, readonly=True,
    #                                states={'draft': [('readonly', False)]}, domain=[('can_request', '=', True)])

    @api.onchange('employee_id')
    def _onchange_employee(self):
        self.depart_id = self.employee_id.department_id
        #self.indenter_no = self.employee_id.identification_id

    @api.one
    def action_cancel(self):
        self.state = 'cancel'

    @api.multi
    def indent_confirm(self):
        super(IndentIndent, self).indent_confirm()

        for indent in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('stock_indent.group_stock_indent_approver')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                indent.message_post(body="This Indent is confirmed.",
                                   partner_ids=partner_ids)

    @api.multi
    def approve_indent(self):
        super(IndentIndent, self).approve_indent()

        for indent in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('stock_indent.group_stock_indent_issuer')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                indent.message_post(body="This Indent is approved.",
                                    partner_ids=partner_ids)

    @api.multi
    def action_view_purchase_requisition(self):
        super(IndentIndent, self).action_view_purchase_requisition()

        for indent in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('stock.group_stock_manager')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                indent.message_post(body="This Indent create purchase requisition.",
                                   partner_ids=partner_ids)

    @api.multi
    def reject_indent(self):
        super(IndentIndent, self).reject_indent()

        for exit in self:
            if exit.employee_id:
                self.message_post(body="Your indent rejected.",
                                  partner_ids=[exit.employee_id.sudo(SUPERUSER_ID).user_id.partner_id.id])

    @api.multi
    def action_view_picking(self):
        result = super(IndentIndent, self).action_view_picking()

        for exit in self:
            if exit.employee_id:
                self.message_post(body="Your indent issue product(s).",
                                  partner_ids=[exit.employee_id.sudo(SUPERUSER_ID).user_id.partner_id.id])

        return result

class IndentProductLines(models.Model):
    _inherit = 'indent.product.lines'

    category_id = fields.Many2one('product.category', string='Product Category',)

    @api.onchange('category_id')
    def onchage_category(self):
        res = {}
        self.product_id = 0
        ids = []
        category = self.env['product.category'].get_categories(self.category_id.id)
        templates = self.env['product.template'].search([('categ_id', 'in', category)])
        for record in templates:
            for rec in record.product_variant_ids:
                ids.append(rec.id)

        res['domain'] = {
            'product_id': [('id', 'in', ids)]
        }
        return res




