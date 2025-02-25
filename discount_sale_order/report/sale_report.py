# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class SaleReport(models.Model):
    _inherit = "sale.report"

    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], string="Discount Type", readonly=True)
    discount = fields.Float('Discount fixed or %', readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['discount_type'] = "l.discount_type"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            l.discount_type"""
        return res
