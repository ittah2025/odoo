# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json


class ReportForQtyInSalesOrder(models.TransientModel):
    _name = "sale.wizard"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    product_ids = fields.Many2many(comodel_name="product.template", relation="product_ids", column1="products", column2="products_i2", string="products", )

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        input_dt = datetime.today()
        res = input_dt.replace(day=1)
        resss = res.date() + relativedelta(day=31)
        rec_start_date = res.date()
        if rec_start_date:
            result["start_date"] = rec_start_date
        if resss:
            result["end_date"] = resss
        return result

    @api.onchange('product_ids')
    def _compute_start_date_end_date(self):
        for rec in self:
            if rec.product_ids:
                input_dt = datetime.today()
                res = input_dt.replace(day=1)
                resss = res.date() + relativedelta(day=31)
                rec.start_date = res.date()
                rec.end_date = resss

    # report with details
    def get_product_ids_report(self):
        domain = []
        list_data = []
        total_data = []
        if self.start_date:
            domain.append(('date_order', '>=', self.start_date))
        if self.end_date:
            domain.append(('date_order', '<=', self.end_date))
        if self.product_ids:
            for p in self.product_ids:
                all_pro = self.env['product.template'].search([('id', '=', p.id)])
                total_qty = 0
                for p in all_pro:
                    pro_qty = self.env['sale.order.line'].search([('product_template_id', '=', p.id)])
                    # custom_date = fields.Date.today()
                    # print('custom_date', custom_date)
                    # amount = 0
                    for r in pro_qty:
                        custom_date = r.order_id.date_order.date()
                        if self.end_date >= custom_date >= self.start_date:
                            total_qty += r.product_uom_qty
                        # amount = r.product_uom_qty
                    # print('total_qty=====', all_pro.name, total_qty, )
                    if total_qty > 0 :
                        # print('r.order_id.date_order', r.order_id.date_order.date(), self.start_date)
                        # if self.end_date >= r.order_id.date_order.date() >= self.start_date:
                        vals_total = {
                            'name': p.name,
                            'total_qty': total_qty,
                        }
                        total_data.append(vals_total)
                    # print('fooor total_lines==', total_data)
                total_qty = 0
                move_linesss = self.env['sale.order.line'].search([('product_template_id', '=', p.id)])
                for w in move_linesss:
                    total_qty += w.product_uom_qty
                for w in move_linesss:
                    custom_date2 = w.order_id.date_order.date()
                    if self.end_date >= custom_date2 >= self.start_date and w.product_uom_qty > 0:
                        vals = {
                            'product': w.product_template_id.name,
                            'sale_name': w.order_id.name,
                            'product_uom_qty': w.product_uom_qty,
                            'date_order': w.order_id.date_order,
                            'linesss': total_data,
                            'total_qty': total_qty,
                        }
                        list_data.append(vals)
        else:
            all_pro = self.env['product.template'].search([])
            for p in all_pro:
                pro_qty = self.env['sale.order.line'].search([('product_template_id', '=', p.id)])
                # custom_date = fields.Date.today()
                # print('custom_date', custom_date)
                # amount = 0
                total_qty = 0
                for r in pro_qty:
                    custom_date = r.order_id.date_order.date()
                    if self.end_date >= custom_date >= self.start_date:
                        total_qty += r.product_uom_qty
                    # amount = r.product_uom_qty
                # print('total_qty=====', all_pro.name, total_qty, )
                if total_qty > 0:
                    # print('r.order_id.date_order', r.order_id.date_order.date(), self.start_date)
                    # if self.end_date >= r.order_id.date_order.date() >= self.start_date:
                    vals_total = {
                        'name': p.name,
                        'total_qty': total_qty,
                    }
                    total_data.append(vals_total)
                print('fooor total_lines==', total_data)
                total_qty = 0
                move_linesss = self.env['sale.order.line'].search([('product_template_id', '=', p.id)])
                for w in move_linesss:
                    custom_date2 = w.order_id.date_order.date()
                    if self.end_date >= custom_date2 >= self.start_date:
                        total_qty += w.product_uom_qty
                if total_qty > 0:
                    for w in move_linesss:
                        custom_date2 = w.order_id.date_order.date()
                        if self.end_date >= custom_date2 >= self.start_date:
                            vals = {
                                'product': w.product_template_id.name,
                                'sale_name': w.order_id.name,
                                'product_uom_qty': w.product_uom_qty,
                                'date_order': w.order_id.date_order,
                                'linesss': total_data,
                                'total_qty': total_qty,
                            }
                            list_data.append(vals)
        data = {
            'move_lines': list_data,
            'all_products': self.product_ids,
            'total_lines': total_data,
            'from': self.start_date,
            'to': self.end_date,
        }
        # print('list_data==', list_data)
        # print('total_lines==', total_data)
        return self.env.ref('kb_report_for_qty_in_sales_order.make_report_wizard_action').report_action(self, data=data)

    # excel button
    # first in print
    def get_returns_report(self):
        #     active_id = self.env.context.get('active_id')
        if self.product_ids:
            print('self.account_id', self.product_ids)
            data = {
                'ids': self.ids,
                'model': self._name,
                'form': {
                    'date_from': self.start_date,
                    'date_to': self.end_date,
                    'product_ids': self.product_ids.ids,
                },
            }
        else:
            all_pro = self.env['product.template'].search([])
            data = {
                'ids': self.ids,
                'model': self._name,
                'form': {
                    'date_from': self.start_date,
                    'date_to': self.end_date,
                    'product_ids': all_pro.ids,
                },
            }
        # print('11 dataaa=', data)
        return self.env.ref('kb_report_for_qty_in_sales_order.returns_excel_report_action').report_action(self, data=data)
