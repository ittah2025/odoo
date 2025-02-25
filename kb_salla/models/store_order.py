from odoo import api, http, exceptions, fields, models, _
import requests
import json
import ast

from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class SallaOrder(models.Model):
    _inherit = 'sale.order'
    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    customerProduct_id = fields.Many2one('product.template', string="Product")

    @api.model
    def create(self, vals):
        res = super(SallaOrder, self).create(vals)
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/orders"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        }
        data = {
            "customer_id": vals.get('partner_id'),

            "shipping_address": {
                # "branch_id": 566146469,
                "country_id": 566146469,
                "city_id": 2097610897,
                "block": "Om El 9823489237",
                "street_number": "jmoh El 8912749823764",
                "address": "building 124234324, floor 212423",
                "postal_code": "23874982374",
                "geocode": "21.4283792, 21.4283792"
            },
            "payment": {
                "status": "paid",
                "method": "credit_card"
            },
            "products": [
                {
                    "id": vals.get("customerProduct_id")
                }
            ]
        }

        vals.get('partner_id')
        if self.env['res.partner'].browse(vals.get('partner_id')).salla_id:
            data.update({
                "customer_id": self.env['res.partner'].browse(vals.get('partner_id')).salla_id
            })

        vals.get('customerProduct_id')
        if self.env['product.template'].browse(vals.get('customerProduct_id')).salla_id:
            data.update({
                "products": [
                    {
                    "id": self.env['product.template'].browse(vals.get('customerProduct_id')).salla_id
                    }
                ]
            })

        # else:
        #     # raise ValidationError(_("Please chose a salla category"))
        #     token = "eJljNYe8-UOGCY1rz05M41Sdrcqd3BUieGUThAv9OJc.ANl6slcCIVRp1Vmww6tphmZ7e0Gkhl8D8v7CORs9ssE"
        #     url = 'https://api.salla.dev/admin/v2/cstomers'

        #     headers = {
        #         'Authorization': f"Bearer {token}",
        #         'Content-Type': "application/json",
        #     }
        #     categ_data = {
        #         "name": self.env['res.partner'].browse(vals.get('customer_id')).name,
        #     }
        #     response = requests.post(url, json=categ_data, headers=headers)
        #     response_data = json.loads(response.text)
        #     id = response_data['data']['id']
        #     salla_customer_id = self.env['res.partner'].browse(vals.get('customer_id')).write({
        #         'salla_id': id
        #     })

        response = requests.post(
            url, json=data, headers=headers)
        response_data = json.loads(response.text)
        id = response_data['data']['id']
        # # # raise ValidationError(
        # # #     _("{}").format(id))
        res.update({
            'salla_id': id,
        })
        return res

    # def write(self, vals):
    #     res = super(SallaOrder, self).write(vals)
    #     if self.salla_id:
    #         data = {
    #             "first_name": self.name,
    #             "last_name": self.last_name,
    #             "mobile": self.mobile,
    #         }
    #         url = 'https://api.salla.dev/admin/v2/customers'
    #         headers = {
    #             'Content-Type': "application/json",
    #             'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #         }
    #         #not working
    #         if vals.get("name"):
    #             data.update({
    #                 "name": self.name,
    #             })
    #         if vals.get("last_name"):
    #             data.update({
    #                 "last_name": self.last_name,
    #             })
    #         url = url + '/' + self.salla_id
    #         response = requests.request(
    #             "PUT", url, headers=headers, data=json.dumps(data))
    #     return res

    def unlink(self):
        if self.salla_id:
            url = 'https://api.salla.dev/admin/v2/orders'
            url = url + '/' + self.salla_id
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            }
            response = requests.request(
                "DELETE", url, headers=headers)
        return super(SallaOrder, self).unlink()