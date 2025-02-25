from odoo import models, fields, api
import requests
import json


class ProductCatgeory(models.Model):
    _inherit = 'product.category'

    salla_id = fields.Char(string="Salla ID", copy=False, readonly=True)
    # representatives = fields.Boolean(string="Representatives")
    

    @api.model
    def create(self, vals):
        res = super(ProductCatgeory, self).create(vals)
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/categories"
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}",
        }
        data = {
            "name": vals.get('name'),
        }
        # if vals['representatives']:
        response = requests.post(url, json=data, headers=headers)
        response_data = json.loads(response.text)
        idd = response_data['data']['id']
        res.update({
            'salla_id': idd,
        })
        return res

    def write(self, vals):
        res = super(ProductCatgeory, self).write(vals)
        if self.salla_id:
            data = {
                "name": self.name,
            }
            token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
            url = 'https://api.salla.dev/admin/v2/categories'
    
            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': "application/json",
            }
            if vals.get('name'):
                data.update({
                    'name': self.name,
                })
            url = url + '/' + self.salla_id
            response = requests.request("PUT", url, headers=headers, data=data)
        return res
    
    def unlink(self):
        if self.salla_id:
            token = 'TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4'
            url = 'https://api.salla.dev/admin/v2/categories' 
            url = url + '/' + self.salla_id

            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': "application/json",
            }
            payload = {}

            response = requests.request(
                "DELETE", url, headers=headers)
        return super(ProductCatgeory, self).unlink()