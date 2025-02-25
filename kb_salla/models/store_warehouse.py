from odoo import api, http, exceptions, fields, models, _
import requests
import json
import ast

from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class SallaWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    # customerFromOdoo = fields.Boolean(string="Customer from Odoo")
    # city_id = fields.Char(string="City ID")
    # country_id = fields.Char(string="Country ID")
    # location = fields.Char(string="Location")
    # type = fields.Char(string="Type(Branch or Warehouse")
    # address_description = fields.Char(string="Address")
    # street = fields.Char(string="Street")
    # local = fields.Char(string="Neighborhood")
    # postal_code = fields.Char(string="Postal code")
    # phone = fields.Char(string="Phone")
    # whatsapp = fields.Char(string="Whatsapp")
    # telephone = fields.Char(string="Telephone")

    @api.model
    def create(self, vals):
        res = super(SallaWarehouse, self).create(vals)
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/branches"
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
        data = {
            "name": "Riyadh",
            "city_id": 2,
            "country_id": 1,
            "branch_city": "Kufa",
            "branch_country": "Saudi Arabia",
            "location": "37.78044939,-97.8503951",
            # "cod_cost": "15",
            "is_cod_available": "on",
            "type": "branch",
            "is_default": "on",
            "address_description": "Riyadh Manfouha Dist",
            "street": "Mansour St.",
            "local": "Riyadh",
            "postal_code": "31952",
            "contacts": {
                "phone": "0552311454",
                "whatsapp": "0552311454",
                "telephone": "0552311454"
            },
            "preparation_time": "05:30",
            "working_hours": {
                "sunday": {
                    "enabled": "on",
                    "from": [
                        "08:00",
                        "15:00"
                    ],
                    "to": [
                        "17:00",
                        "23:30"
                    ]
                },
                "monday": {
                    "enabled": "on",
                    "from": [
                        "08:00",
                        "19:00"
                    ],
                    "to": [
                        "17:00",
                        "23:30"
                    ]
                }
            }
        }
        response = requests.post(
            url, json=data, headers=headers)
        response_data = json.loads(response.text)
        id = response_data['data']['id']

        res.update({
            'salla_id': id,
        })
        return res

    # def write(self, vals):
    #     res = super(SallaWarehouse, self).write(vals)
    #     if self.salla_id:
    #         data = {
    #             "first_name": self.name,
    #             "last_name": self.last_name,
    #             "mobile": self.mobile,
    #         }
    #         url = 'https://api.salla.dev/admin/v2/branches'
    #         headers = {
    #             'Content-Type': "application/json",
    #             'Authorization': "Bearer eJljNYe8-UOGCY1rz05M41Sdrcqd3BUieGUThAv9OJc.ANl6slcCIVRp1Vmww6tphmZ7e0Gkhl8D8v7CORs9ssE"
    #         }
    #         # not working
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
# #ban customer
#     def write(self, vals):
#         res = super(ResPartner, self).write(vals)
#         if self.salla_id:
#             data = {
#                 "reason": vals['name'],
#                 "last_name": self.name,
#                 "mobile": self.mobile,
#             }
#             url = 'https://api.salla.dev/admin/v2/customers/blacklist'
#             headers = {
#                 'Content-Type': "application/json",
#                 'Authorization': "Bearer eJljNYe8-UOGCY1rz05M41Sdrcqd3BUieGUThAv9OJc.ANl6slcCIVRp1Vmww6tphmZ7e0Gkhl8D8v7CORs9ssE"
#             }
#             if vals.get("mobile"):
#                 data.update({
#                     "mobile": self.mobile,
#                 })
#             if vals.get("name"):
#                 data.update({
#                     "name": self.name,
#                 })
#             # if vals.get("mobile"):
#             #     data.update({
#             #         "mobile": self.mobile,
#             #     })
#             url = url + '/' + self.salla_id
#             response = requests.request(
#                 "PUT", url, headers=headers, data=json.dumps(data))
#         return res

    def unlink(self):
        if self.salla_id:
            url = 'https://api.salla.dev/admin/v2/branches'
            url = url + '/' + self.salla_id
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            }
            response = requests.request(
                "DELETE", url, headers=headers)
        return super(SallaWarehouse, self).unlink()
