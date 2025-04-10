# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BookName(models.TransientModel):
    """Defining Book Name."""

    _name = "book.name"
    _description = "Book Name"

    name = fields.Many2one("product.product", "Book Name", required=True)
    card_id = fields.Many2one("library.card", "Card No", required=True)

    def create_new_books(self):
        for rec in self:
            rec.create({"name": rec.name.id, "card_id": rec.card_id.id})
