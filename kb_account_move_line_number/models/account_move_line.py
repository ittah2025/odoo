from odoo import models, api, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    number = fields.Integer(
        compute='_compute_get_number',
        store=True,
    )

    @api.depends('sequence', 'move_id')
    def _compute_get_number(self):
        for order in self.mapped('move_id'):
            number = 1
            for line in order.invoice_line_ids:
                line.number = number
                number += 1
