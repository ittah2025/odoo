from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    kb_allStock = fields.Float(string='All Stock Number', required=True)