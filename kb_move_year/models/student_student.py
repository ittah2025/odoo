from email.policy import default
from odoo import models, fields,api
from datetime import datetime
from nis import match
from unittest import case
from hijri_converter import Hijri, Gregorian

# from translate import Translator



class students(models.Model):
    
            
    _inherit = "student"

    
   