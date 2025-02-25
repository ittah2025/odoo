# -*- coding: utf-8 -*-


import pytz
import time
from operator import itemgetter
from itertools import groupby
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, date


class NMDataAuditReport(models.AbstractModel):
    _name = 'report.nm_stock_reports.asset_report'
    _description = "Report Asset"

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('kb_account_asset_reports.data_audit_template.xml')
        record_id = data['id'] if data and data['id'] else docids[0]
        records = self.env['asset.report.wizard'].browse(record_id)
        return {
           'doc_model': report.model,
           'docs': records,
        }
