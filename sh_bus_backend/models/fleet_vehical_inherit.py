# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class FleetVehicalInherit(models.Model):
    _inherit = 'fleet.vehicle'

    reg_no = fields.Char(string="Registration No.")
    fleet_type = fields.Many2one('sh.bus.type', string="Fleet Type")
    engine_no = fields.Char(string="No Engine")
    owner = fields.Many2one("res.partner", string="Owner")
    amenities_ids = fields.Many2many("sh.bus.amenities", string='Amenities')
    brand = fields.Many2one('sh.bus.brand', string="Brands")
    status = fields.Selection([('registered', 'Registered'), (
        'downgraded', 'Downgraded')], string='Status', readonly=True, copy=False)
