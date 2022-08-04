from odoo import api, fields, tools, models, _


class TemplateType(models.Model):
    _name = 'template.type'
    _description = 'Template Type'

    name = fields.Char('Name',)
    template = fields.Text("Template ")