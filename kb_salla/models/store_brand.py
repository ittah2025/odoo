from odoo import api, http, exceptions, fields, models, _
import requests
import json
import ast

from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class SallaBrand(models.Model):
    _inherit = 'stock.warehouse'
    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    description = fields.Char(string="Description")
    banner = fields.Char(string="Banner")
    logo = fields.Char(string="Logo")

    @api.model
    def create(self, vals):
        res = super(SallaBrand, self).create(vals)
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/brands"
        headers = {
            'Content-Type': "",
            'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4",
            'content-type': "multipart/form-data; boundary=---011000010111000001101001"
        }
        # data = {
        #     "name": vals['name'],
        #     "description": vals['description'],
        #     "banner": "https://i0.wp.com/www.lusakatimes.com/wp-content/uploads/2018/04/pepperoni-pizza.jpg",
        #     "logo": "https://i0.wp.com/www.lusakatimes.com/wp-content/uploads/2018/04/pepperoni-pizza.jpg",
        # }
        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"logo\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"banner\"\r\n\r\n\r\n-----011000010111000001101001--\r\n\r\n"

        response = requests.post(
            url, json=payload, headers=headers)
        response_data = json.loads(response.text)
        id = response_data['data']['id']
        # raise ValidationError(
        #     _("{}").format(id))
        res.update({
            'salla_id': id,
        })
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

    # def unlink(self):
    #     if self.salla_id:
    #         url = 'https://api.salla.dev/admin/v2/brands'
    #         url = url + '/' + self.salla_id
    #         headers = {
    #             'Content-Type': "application/json",
    #             'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
    #         }
    #         response = requests.request(
    #             "DELETE", url, headers=headers)
    #     return super(SallaBrand, self).unlink()
