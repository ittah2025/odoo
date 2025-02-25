# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 OM Apps 
#    Email : omapps180@gmail.com
#################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    excel_bg_color = fields.Char('Background Color', related='company_id.excel_bg_color', readonly=False)
    bg_font_color = fields.Char('Bg Font Color', related='company_id.bg_font_color', readonly=False)
    
    po_excel_bg_color = fields.Char('Background Color', related='company_id.po_excel_bg_color', readonly=False)
    po_bg_font_color = fields.Char('Bg Font Color', related='company_id.po_bg_font_color', readonly=False)
    
    inv_excel_bg_color = fields.Char('Background Color', related='company_id.inv_excel_bg_color', readonly=False)
    inv_bg_font_color = fields.Char('Bg Font Color', related='company_id.inv_bg_font_color', readonly=False)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
