from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    is_anl_required = fields.Boolean(string="Analytic Account Required")
    is_partner_required = fields.Boolean(string="Partner Account Required")
    is_anl_tag_required = fields.Boolean(string="Analytic Tags Required")