from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ChangeableAllowance(models.TransientModel):
    _name = "changeable_allowance"
    _description = "Changeable Allowance"

    contract_ids = fields.Many2many("hr.contract", string="Contracts")

    @api.model
    def default_get(self, fields):
        res = super(ChangeableAllowance, self).default_get(fields)

        contracts = self.env["hr.contract"].search([('state', '=', 'open')])
        res["contract_ids"] = [(6, 0, contracts.ids)]
        return res

