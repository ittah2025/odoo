from odoo import api, http, exceptions, fields, models, _
import requests
import json
import ast

from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    # customerFromOdoo = fields.Boolean(string="Customer from Odoo")
    last_name = fields.Char(string="Last Name")

    # @api.model
    # def create(self, vals):
    #     res = super(ResPartner, self).create(vals)
    #     token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #     url = "https://api.salla.dev/admin/v2/customers"
    #     headers = {
    #         'Content-Type': "application/json",
    #         'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #     }
    #     data = {
    #         "first_name": vals['name'],
    #         "last_name": vals['last_name'],
    #         "mobile": vals.get('mobile'),
    #         "mobile_code": "967",
    #         "mobile_code_country": "SA",

    #         # "email": vals['email'],
    #         # "groups": vals['groups'],
    #         # "email": vals['email'],
    #         # "phone": vals['phone'] or vals['mobile'],
    #         # "tax_number": vals['vat'],
    #         # "location_verified": 'true',
    #         # 'financials': {'credit_limit': vals.get('credit_limit_compute')},
    #         # 'city': vals['city'],
    #         # 'lat': vals['loc_lat'],
    #         # 'lng': vals['loc_lang'],
    #         # 'assigned_to': employee_repzo.salla_id,
    #         # 'country': self.env['res.country'].browse(vals['country_id']).name if vals['country_id'] else None,
    #         # 'zip': vals['zip'],
    #         # 'state': self.env['res.country.state'].browse(vals['state_id']).name if vals['state_id'] else None,
    #         # 'credit_limit': vals.get('credit_limit_compute')
    #     }

    #     # if vals['customerFromOdoo']:
    #     response = requests.post(
    #         url, json=data, headers=headers)
    #     response_data = json.loads(response.text)
    #     id = response_data['data']['id']
    #     # raise ValidationError(
    #     #     _("{}").format(id))
    #     res.update({
    #         'salla_id': id,
    #     })
    #     return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if self.salla_id:
            data = {
                "first_name": self.name,
                "last_name": self.last_name,
                "mobile": self.mobile,
            }
            url = 'https://api.salla.dev/admin/v2/customers'
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer eJljNYe8-UOGCY1rz05M41Sdrcqd3BUieGUThAv9OJc.ANl6slcCIVRp1Vmww6tphmZ7e0Gkhl8D8v7CORs9ssE"
            }
            #not working
            if vals.get("name"):
                data.update({
                    "name": self.name,
                })
            if vals.get("last_name"):
                data.update({
                    "last_name": self.last_name,
                })
            url = url + '/' + self.salla_id
            response = requests.request(
                "PUT", url, headers=headers, data=json.dumps(data))
        return res
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
            url = 'https://api.salla.dev/admin/v2/customers'
            url = url + '/' + self.salla_id
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer eJljNYe8-UOGCY1rz05M41Sdrcqd3BUieGUThAv9OJc.ANl6slcCIVRp1Vmww6tphmZ7e0Gkhl8D8v7CORs9ssE"
            }
            response = requests.request(
                "DELETE", url, headers=headers)
        return super(ResPartner, self).unlink()
