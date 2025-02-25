from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_anl_required = fields.Boolean(string="Analytic Account Required",
                                     related='account_id.is_anl_required')
    is_partner_required = fields.Boolean(string="Partner Account Required",
                                     related='account_id.is_partner_required')
    is_anl_tag_required = fields.Boolean(string="Analytic Tags Required",
                                     related='account_id.is_anl_tag_required')