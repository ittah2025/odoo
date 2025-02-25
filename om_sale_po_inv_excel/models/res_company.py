# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 OM Apps 
#    Email : omapps180@gmail.com
#################################################

from odoo import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    
    excel_bg_color = fields.Char('Background Color', default='#c79816')
    bg_font_color = fields.Char('Bg Font Color', default='#FFFFFF')
    
    po_excel_bg_color = fields.Char('Background Color', default='#c79816')
    po_bg_font_color = fields.Char('Bg Font Color', default='#FFFFFF')
    
    
    inv_excel_bg_color = fields.Char('Background Color', default='#c79816')
    inv_bg_font_color = fields.Char('Bg Font Color', default='#FFFFFF')




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

