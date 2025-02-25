from odoo import api, exceptions, fields, models, _
from odoo.exceptions import ValidationError
import requests
import json
import ast
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class ProductTemplateSalla(models.Model):
    _inherit = 'product.template'

    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    # representatives = fields.Boolean(string="Representatives")
    calories = fields.Char(string="Calories")
    quantity = fields.Char(string="Quantity")
    product_type = fields.Char(string="Product type")
    weight = fields.Char(string="Weight")
    weight_type = fields.Char(string="Weight type")
    cost_price = fields.Float(string="Cost Price")
    sku = fields.Char(string="sku")
    sale_end = fields.Date(string="End of Sale")
    gtin = fields.Char(string="gtin")
    mpn = fields.Char(string="mpn")
    maximum_quantity_per_order = fields.Integer(
        string="Max Quanitiy per Customer")
    original = fields.Char(string="Attach Image URL")

    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplateSalla, self).create(vals)
    #     token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #     url = "https://api.salla.dev/admin/v2/products"
    #     headers = {
    #         'Content-Type': "application/json",
    #         'Authorization': f"Bearer {token}",
    #     }
    #     data = {
    #         "name": vals.get('name'),
    #         "price": vals.get('list_price'),
    #         "product_type": vals.get('product_type'),
    #         # "product_type": "food",
    #         "calories": vals.get('calories'),
    #         "quantity": vals.get('quantity'),
    #         "weight": vals.get('weight'),
    #         "cost_price": vals.get('cost_price'),
    #         "sku": vals.get('sku'),
    #         "sale_end": vals.get('sale_end'),
    #         "maximum_quantity_per_order": vals.get('maximum_quantity_per_order'),
    #         "weight_type": vals.get('weight_type'),
    #         "categories": [
    #             vals.get('categ_id'),
    #         ],
    #         "images": [
    #             {
    #                 "original": vals.get('original'),
    #             }
    #         ],
    #     }
    #     # elif vals['product_type'] == "service":
    #     #     data = {
    #     #         "name": vals['name'],
    #     #         "price": vals['list_price'],
    #     #         "product_type": vals['product_type'],
    #     #         "quantity": vals.get('quantity'),
    #     #         "weight": vals['weight'],
    #     #         "cost_price": vals.get('cost_price'),
    #     #         "sku": vals.get('sku'),
    #     #         "sale_end": vals.get('sale_end'),
    #     #         "maximum_quantity_per_order": vals.get('maximum_quantity_per_order'),
    #     #         "weight_type": vals.get('weight_type'),
    #     #         "categories": [
    #     #             vals.get('categ_id'),
    #     #         ],
    #     #         "images": [
    #     #             {
    #     #                 "original": vals.get('original'),
    #     #             }
    #     #         ],
    #     #     }
    #     # elif vals['product_type'] == "digital" or vals['product_type'] == "group_products" or vals['product_type'] == "codes" or vals['product_type'] == "product" or vals['product_type'] == "donating":
    #     #     data = {
    #     #         "name": vals['name'],
    #     #         "price": vals['list_price'],
    #     #         "product_type": vals['product_type'],
    #     #         "quantity": vals.get('quantity'),
    #     #         "weight": vals['weight'],
    #     #         "cost_price": vals.get('cost_price'),
    #     #         "sku": vals.get('sku'),
    #     #         "sale_end": vals.get('sale_end'),
    #     #         "gtin": vals.get('gtin'),
    #     #         "mpn": vals.get('mpn'),
    #     #         "maximum_quantity_per_order": vals.get('maximum_quantity_per_order'),
    #     #         "weight_type": vals.get('weight_type'),
    #     #         "categories": [
    #     #             vals.get('categ_id'),
    #     #         ],
    #     #         "images": [
    #     #             {
    #     #                 "original": vals.get('original'),
    #     #             }
    #     #         ],
    #     #     }
    #     if vals.get('categ_id'):
    #         if self.env['product.category'].browse(vals.get('categ_id')).salla_id:
    #             data.update({
    #                 "categories": [
    #                     self.env['product.category'].browse(
    #                         vals.get('categ_id')).salla_id
    #                 ]
    #             })
    #             salla_categ_id = self.env['product.category'].browse(
    #                 vals.get('categ_id'))

    #     else:
    #         # raise ValidationError(_("Please chose a salla category"))
    #         token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #         url = 'https://api.salla.dev/admin/v2/products'

    #         headers = {
    #             'Authorization': f"Bearer {token}",
    #             'Content-Type': "application/json",
    #         }
    #         categ_data = {
    #             "name": self.env['product.category'].browse(vals.get('categ_id')).name,
    #         }
    #         response = requests.post(url, json=categ_data, headers=headers)
    #         response_data = json.loads(response.text)
    #         idd = response_data['data']['id']
    #         salla_categ_id = self.env['product.category'].browse(vals.get('categ_id')).write({
    #             'salla_id': idd
    #         })

    #     # if vals['representatives']:
    #     response = requests.post(
    #         url, json=data, headers=headers)
    #     response_data = json.loads(response.text)

    #     id = response_data['data']['id']
    #     res.update({
    #         'salla_id': id,
    #     })
    #     return res

    def write(self, vals):
        res = super(ProductTemplateSalla, self).write(vals)
        if self.salla_id:
            data = {
                "name": self.name,
                "price": self.list_price,
                "quantity": self.quantity,
            }
            token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            url = 'https://api.salla.dev/admin/v2/products'

            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': "application/json",
            }
            if vals.get("name"):
                data.update({
                    "name": self.name,
                })
            if vals.get("list_price"):
                data.update({
                    "price": self.list_price,
                })
            if vals.get("quantity"):
                data.update({
                    "quantity": self.quantity,
                })
            if vals.get("calories"):
                data.update({
                    "calories": self.calories,
                })
            if vals.get("cost_price"):
                data.update({
                    "cost_price": self.cost_price,
                })
            if vals.get("sale_end"):
                data.update({
                    "sale_end": self.sale_end,
                })
            if vals.get("maximum_quantity_per_order"):
                data.update({
                    "maximum_quantity_per_order": self.maximum_quantity_per_order,
                })
            if vals.get("weight"):
                data.update({
                    "weight": self.weight,
                })
            if vals.get("weight_type"):
                data.update({
                    "weight_type": self.weight_type,
                })
            if vals.get("sku"):
                data.update({
                    "sku": self.sku,
                })
        #         if vals.get("mpn"):
        #             data.update({
        #                 "mpn": self.mpn,
        #             })
            if vals.get("gtin"):
                data.update({
                    "gtin": self.gtin,
                })
            if vals.get("original"):
                data.update({
                    "original": self.original,
                })

            url = url + '/' + self.salla_id
            response = requests.request(
                "PUT", url, headers=headers, data=json.dumps(data))
        return res

    def unlink(self):
        if self.salla_id:
            token = 'TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4'
            url = 'https://api.salla.dev/admin/v2/products'
            url = url + '/' + self.salla_id

            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': "application/json",
            }
            payload = {}

            response = requests.request(
                "DELETE", url, headers=headers)
        return super(ProductTemplateSalla, self).unlink()
