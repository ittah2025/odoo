from odoo import models, fields,api
from datetime import date
from xml.dom import ValidationErr
from datetime import datetime, timedelta
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        compute='_compute_journal_id', store=True, readonly=False, precompute=True,
        required=True,
        states={'draft': [('readonly', False)]},
        check_company=True,
        domain="[]",
    )