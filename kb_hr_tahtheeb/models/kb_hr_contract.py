from odoo import api, fields, models, _


class HrContract(models.Model):
    _inherit = "hr.contract"

    kb_Transportation_allowance = fields.Float(string='Transportation Allowance')
    other_allowance = fields.Char(string='Transportation Allowance')
