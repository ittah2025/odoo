from odoo import api, fields, models,_
from datetime import date
import datetime

class kb_CR_No(models.Model):
  _inherit = 'res.partner'

  kb_Num_Commercial_Registration = fields.Char("Commercial Registration Number" )
