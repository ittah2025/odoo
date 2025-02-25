# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, datetime
from odoo.exceptions import  ValidationError
from odoo import _

class hremployee(models.Model):
  _inherit = "hr.employee"
 
  nameEnglish = fields.Char( string='English Name')
  haspassport=fields.Boolean(string='has license or not?')
  releaseDate = fields.Date(string='Release Date')
  Explicense = fields.Date(string='Exp')

  Sizebantallon= fields.Selection([
        ('sx', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', '2XL'),
        ] ,string='Size pants')
  Sizeblouse= fields.Selection([
        ('sx', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', '2XL'),
        ] ,string='Size blouse')
  Sizeshoes = fields.Char(string='Size Shoes')

  bus=fields.Boolean(string='')
  coaster=fields.Boolean(string='')

  Expbank = fields.Date(string='Expiry date of Bank card')

  Exp = fields.Date(string='Expiry date of residence or passport')

  file1 = fields.Binary("Medical Examination")
  file1_name = fields.Char('Medical Examination')
  Exp_medical  = fields.Date(string='When does the medical examination end?')
 

  note = fields.Text(string='Note')


  show=fields.Boolean(default=False)
  streett= fields.Char(string='Street')
  street22= fields.Char(string='Street2')
  cityy= fields.Char(string='City')
  state_idd= fields.Many2one('res.country.state', string='State')
  zipp = fields.Char(string='Zip')
  country_idd= fields.Many2one('res.country', string='Country')

  @api.onchange('bus','coaster')
  def change_fun(self):
      for rec in self:
        if rec.bus == True:
          rec.coaster = False 
        elif rec.bus == False:
          rec.coaster = True 

  driver_number = fields.Char(string="Driver Number")
  driver_release_date = fields.Date(string="Driver Release date")
  driver_expiry_date = fields.Date(string="Driver expiry date")




    
  
    
  