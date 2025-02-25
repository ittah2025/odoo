from odoo import models, fields,_

class kb_hr(models.Model):
    _inherit = "hr.employee"

class resCompany(models.Model):
    _inherit = "res.company"

    kb_userName = fields.Many2one('res.users', String='Representative')
