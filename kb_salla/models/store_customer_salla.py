from odoo import api, exceptions, fields, models, _
import requests
import json
import ast
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class respartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create_customer(self):
        url = "https://api.salla.dev/admin/v2/customers"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        }
        response = requests.request("GET", url, headers=headers)
        customer_report = response.json()
        # looping inside the JSON data to fetch customer ID's
        cstCount = 0
        for customer in customer_report['data']:
            # type-casting ID from integer to string to match the appropriate format for comparison
            customerId = str(customer['id'])
            partner_check = self.env['res.partner'].search(
                [('salla_id', '=', customerId)])
            # partner_check gives the url ID's of customers in Odoo that match with the salla ID of customers in Salla
            # we check if there's is an existing ID
            if len(partner_check) == 0:
                cstCount = + 1
                # in case of customer not existing on Odoo, we create it
                import_cstmr = self.env['res.partner'].create(
                    {
                        'name': customer['first_name'],
                        'last_name': customer['last_name'],
                        'mobile': customer['mobile'],
                        'salla_id': customer['id'],
                    })
                # we continue the loop if partner_check gives us an ID and don't create a customer in Odoo
            else:
                continue
        return cstCount
