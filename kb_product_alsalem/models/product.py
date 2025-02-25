from odoo import models, fields,api
from datetime import date
from xml.dom import ValidationErr
from datetime import datetime, timedelta


class product(models.Model):
    # _name = "products"
    _inherit = "product.template"
    
    # Product Fields:
    length = fields.Float(string='الطول')
    width = fields.Float(string='العرض')
    height = fields.Float(string='الأرتفاع')

    # Dimension Fields:
    Dimension = fields.Char()
    dimensionL = fields.Float(string='الطول')
    dimensionW = fields.Float(string='العرض')
    dimensionH = fields.Float(string='الأرتفاع')

    # Diameter Inlet Fields:
    Diameter = fields.Char()
    diameterInletI = fields.Char(string='داخل')
    diameterOutletI = fields.Char(string='خارج')

    # Diameter Outlet Fields:
    diameterInletO = fields.Char(string='داخل')
    diameterOutletO = fields.Char(string='خارج')

    # Condition Fields:
    Condition = fields.Char()
    newC = fields.Char(string='جديد')
    usedC = fields.Char(string='مستخدم')
    remanufacturedC = fields.Char(string='اعادة التصنيع')