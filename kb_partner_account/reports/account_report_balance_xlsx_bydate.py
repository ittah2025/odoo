# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class PartnerXlsxBydate(models.AbstractModel):
    _name = 'report.kb_partner_account.report_balance_xlsx_bydate'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):


            # One sheet by partner
        sheet = workbook.add_worksheet("any")
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, obj.name, bold)