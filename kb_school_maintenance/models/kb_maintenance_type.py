from odoo import api, fields, tools, models, _




class maintenanceType(models.Model):
    _name = 'kb.maintenance.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Information'
    _rec_name = 'kb_maintenanceTypeName'

    kb_maintenanceTypeName = fields.Char(string='Maintenance Type', traking=True)