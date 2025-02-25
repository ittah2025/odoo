from venv import create
from odoo import api, exceptions, fields, models, _
import requests
import json
import ast
import time
import schedule
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)

class productcategory(models.Model):
    _inherit = 'product.category'
    
    @api.model
    def create_category(self):
        token = "TTJtWJG2IcKD1DdusJAqYHYYT4A8nZjrepC1VzZEUMo.k_3CcL0E3pE67beagtXvMh-hy_ibWJ2yIoyzOU_x1e4"
        url = "https://api.salla.dev/admin/v2/categories"
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}",
        }
        response = requests.request("GET", url, headers=headers)    
        
        category_report = response.json()
        
        # i = 0
        for category in category_report['data']:
            category_check = self.env['product.category'].search([( 'salla_id','=', category['id'])])
            if not category_check:
                categ_id = self.env['product.category'].create(    
                            {
                            'name': category['name'],
                            'salla_id': category['id'],
                            })
            else:
                pass
