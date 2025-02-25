from odoo import api, exceptions, fields, models, _
import requests
import json
import ast
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class ProductTemplateOdooSalla(models.Model):
    _inherit = 'product.template'

    @api.model
    def create_product(self):
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/products"
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}",
        }
        response = requests.request("GET", url, headers=headers)

        salla_report = response.json()

        # i = 0
        for product in salla_report['data']:
            if 'product_type' == "food":
                emp_id = {
                    'name': product['name'],
                    'list_price': product['price']['amount'],
                    'product_type': "food",
                    'calories': product['calories'],
                    'quantity': product['quantity'],
                    'weight': product['weight'],
                    'cost_price': product['cost_price'],
                    'sku': product['sku'],
                    'sale_end': product['sale_end'],
                    'maximum_quantity_per_order': product['maximum_quantity_per_order'],
                    'weight_type': product['weight_type'],
                    'categ_id': 582430292,
                    # 'original':product['original'],
                    # "images": [
                    #     {
                    #         "original": product['original'],
                    #     }
                    # ],
                    'salla_id': product['id'],
                }
                # elif product['product_type'] == "service":
            # raise ValidationError(_("{},").format(emp_id))
            # try:
            # product_check = self.env['product.template'].search(
            #     [('salla_id', '=', product['id'])])
            # # category = self.env['product.category'].search([( 'categ_id','=', product['category'])])

            # if not product_check:
            #     # if product['product_type'] == "food":
            #     emp_id = self.env['product.template'].create({
            #         'name': product['name'],
            #         'list_price': product['price']['amount'],
            #         'product_type': 'food',
            #         'calories': product['calories'],
            #         'quantity': product['quantity'],
            #         'weight': product['weight'],
            #         'cost_price': product['cost_price'],
            #         'sku': product['sku'],
            #         'sale_end': product['sale_end'],
            #         'maximum_quantity_per_order': product['maximum_quantity_per_order'],
            #         'weight_type': product['weight_type'],
            #         'categ_id': 582430292,
            #         # 'original':product['original'],
            #         # "images": [
            #         #     {
            #         #         "original": product['original'],
            #         #     }
            #         # ],
            #         'salla_id': product['id'],
            #     })
            # #     # elif product['product_type'] == "service":
            # #     #     emp_id = self.env['product.template'].create({
            # #     #         'name': product['name'],
            # #     #         'list_price': product['price'],
            # #     #         'product_type': product['product_type'],
            # #     #         'gtin': product['gtin'],
            # #     #         'quantity': product['quantity'],
            # #     #         'weight': product['weight'],
            # #     #         'cost_price': product['cost_price'],
            # #     #         'sku': product['sku'],
            # #     #         'sale_end': product['sale_end'],
            # #     #         'maximum_quantity_per_order': product['maximum_quantity_per_order'],
            # #     #         'weight_type': product['weight_type'],
            # #     #         'categ_id': product['categories'],
            # #     #         # 'original':product['original'],
            # #     #         "images": [
            # #     #             {
            # #     #                 "original": product['original'],
            # #     #             }
            # #     #         ],
            # #     #         'salla_id': product['id'],
            # #     #     })

            # else:
            #     pass

            # _logger.info('line number %s\n\n\n ', i)
            # i += 1
            # except:
            #     raise ValidationError(_("{},\n{}").format(i, product['barcode']))
