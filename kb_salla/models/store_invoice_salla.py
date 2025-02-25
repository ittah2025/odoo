from odoo import api, exceptions, fields, models, _
import requests
import json
import ast
import time
# import schedule
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta
_logger = logging.getLogger(__name__)


class SallaInvoice(models.Model):
    _inherit = 'sale.order'

    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)

    @api.model
    def create_invoice(self):
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/orders"
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
        response = requests.request("GET", url, headers=headers)
        orders_report = response.json()
        invCount = 0
        for orderId in orders_report['data']:

            token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            url = "https://api.salla.dev/admin/v2/orders"
            url = url + '/' + str(orderId['id'])

            response = requests.request("GET", url, headers=headers)
            order_inv = response.json()

            token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            url = "https://api.salla.dev/admin/v2/orders/invoices"
            response = requests.request("GET", url, headers=headers)
            inv_report = response.json()

            for invId in inv_report['data']:
                token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
                url = "https://api.salla.dev/admin/v2/orders/invoices"
                url = url + '/' + str(invId['id'])
                response = requests.request(
                    "GET", url, headers=headers)
                inv = response.json()
                # for inv_exs in inv['data']:
                invnum = inv['data']['invoice_number']
                invdate = (order_inv['data']['date']['date'])[:10]
                inv_exs = self.env['account.move'].search(
                    [('name', '=', invnum)])
                if len(inv_exs) == 0:
                    sallaCustomer = str(order_inv['data']['customer']['id'])
                    # raise ValidationError(("{}").format((sallaCustomer)))
                    partner = self.env['res.partner'].search(
                        [('salla_id', '=', sallaCustomer)])
                    # raise ValidationError(("{}").format((partner.id)))
                    if len(partner) == 1:
                        sale_id = self.env['sale.order'].create({
                            'name': invnum,
                            'partner_id': partner.id,  # partner.id,
                            'date_order': invdate,
                            # 'warehouse_id': 12,
                            # 'commitment_date': '12-05-2022 17:50:44'
                            'client_order_ref':  invnum,
                        })
                    else:
                        continue
                else:
                    continue

                sale_order_line = []
                invCount += 1
                for i in order_inv['data']['items']:
                    product_salla = self.env['product.product'].search(
                        [('salla_id', '=', i['product']['id'])])
                    sale_order_line.append(self.env['sale.order.line'].create({
                        'product_id': product_salla.id,
                        # 'product_uom': 12,
                        'product_uom_qty': i['quantity'],
                        'name': "Delicious Meal",
                        # 'tax_id': ,

                        # / 1000,
                        'price_unit': i['product']['price']['amount'],
                        'order_id': sale_id.id
                    })
                    )
                sale_id.action_confirm()
                sale_id._create_invoices()
                for invoice in sale_id.invoice_ids:
                    invoice.name = invnum
                    invoice.invoice_date = invdate

                    invoice.action_post()
                    invoice.action_register_payment()

                    invoice_obj = self.env['account.move'].search(
                        [('invoice_origin', '=', sale_id.name)])
                    payment = invoice.env['account.payment']

                    payment_method = invoice.env['account.payment.method'].search(
                        [], limit=1)

                    for inv in invoice_obj:
                        to_reconcile = []
                        payment_order = payment.create({
                            'name': inv.name,
                            'partner_id': inv.partner_id.id,
                            'amount': inv.amount_total,
                            'payment_type': 'inbound',
                            'partner_type': 'customer',
                            'payment_method_id': payment_method.id,
                            'payment_method_line_id': payment_method.id,
                            'journal_id': 1,
                            'invoice_date': '2022-05-22',  # date.today() - timedelta(days = 1 ), #date.today(),
                            # invoices['issue_date'],
                            # 'invoice_datetime': inv.name,
                            'ref':  inv.name,
                        })

                        sequence_code = 'account.payment.customer.invoice'
                        # todo: if statement goes here to check that invoice is
                        inv.action_invoice_paid()
                        pay_confirm = payment = invoice.env['account.payment'].search(
                            [("ref", "=", inv.name)])
                        pay_confirm.action_post()
                        to_reconcile.append(inv.line_ids)
                        domain = [('account_internal_type', 'in',
                                   ('receivable', 'payable')), ('reconciled', '=', False)]
                        for payment, lines in zip(pay_confirm, to_reconcile):
                            payment_lines = payment.line_ids.filtered_domain(
                                domain)
                            for account in payment_lines.account_id:
                                (payment_lines + lines)\
                                    .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
                                    .reconcile()

                            # return pay_confirm
                    # for picking in sale_id.picking_ids:

                    #     picking.action_assign()
                    #     picking.action_set_quantities_to_reservation()
                    #     picking.action_confirm()
                    #     picking.button_validate()
                break

        return invCount  # sale_order_line
