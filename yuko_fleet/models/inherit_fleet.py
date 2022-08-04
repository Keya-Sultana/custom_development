from odoo import api, fields, models, tools, _


class InheritFleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fuel_type = fields.Selection([('diesel', 'Diesel'), ('octane', 'Octane'), ('patrol', 'Patrol'), ('lpg', 'LPG'), ('cng', 'CNG')], 'Fuel Type', help='Fuel Used by the vehicle')
