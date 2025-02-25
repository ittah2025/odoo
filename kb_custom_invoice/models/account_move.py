# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Created By Mujtaba
    # kb_datetime = fields.Datetime(string="Confirm date")
    #
    # def action_post(self):
    #     res = super(AccountMove, self).action_post()
    #     utc_time = datetime.utcnow()
    #     time_now = utc_time.strftime('%H:%M:%S')
    #     for record in self:
    #         if not record.kb_datetime:
    #
    #             if not record.invoice_date:
    #                 record.invoice_date = utc_time.date()
    #
    #             invoice_date = record.invoice_date.strftime('%Y-%m-%d')
    #             record.write({'kb_datetime': invoice_date + ' ' + time_now})
    #     return res