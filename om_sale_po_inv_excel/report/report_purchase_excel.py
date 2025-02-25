# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 OM Apps 
#    Email : omapps180@gmail.com
#################################################


from odoo import models, fields, api, _
from odoo.modules.module import get_module_resource
import io
from PIL import Image
import base64
om_bg_color = '#c79816'
om_font_color = '#FFFFFF'

class PurchaseXlsx(models.AbstractModel):
    _name = 'report.om_sale_po_inv_excel.om_purchase_excel_report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def get_resized_image_data(self, file_path, bound_width_height):
        # get the image and resize it
        im = Image.open(file_path)
        im.thumbnail(bound_width_height, Image.ANTIALIAS)  # ANTIALIAS is important if shrinking

        # stuff the image data into a bytestream that excel can read
        im_bytes = io.BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes
    
    
    def get_image(self,obj):
        image_path = get_module_resource('om_sale_po_inv_excel', 'static', 'logo.png')
        fh = open(image_path, "wb")
        fh.write(base64.decodebytes(obj.company_id.logo))
        fh.close()
        bound_width_height = (100 , 100)
        image_data = self.get_resized_image_data(image_path, bound_width_height)
        return image_path, image_data
        
    def get_address(self,company):
        address = ''
        if company.name:
            address = company.name + '\n'
        if company.street:
            address = address + company.street + '\n'
        if company.street2:
            address = address + company.street2 + '\n'
        if company.city:
            city = company.city
            if company.zip:
                city = city + '  '+ company.zip
            
            address = address + city + '\n'
        if company.country_id:
            address = address + company.country_id.name + '\n'
        
        return address
            
        
            
    def set_company_header(self,workbook,sheet, obj):
        company_formate = workbook.add_format({'font_size':10,'align':'left','valign':'vcenter', 'border':True})
        image_path, image_data = self.get_image(obj)
        sheet.insert_image('G2', image_path,{'image_data': image_data})
        company_address = self.get_address(obj.company_id)
        sheet.merge_range(0,0,4,7,company_address, company_formate)
        
    def set_company_footer(self,workbook,sheet, obj,row):
        footer = ''
        company_id = obj.company_id
        if company_id:
            if company_id.phone:
                footer = 'Phone : '+company_id.phone
            
            if company_id.email:
                if footer:
                    footer = footer + ' | '
                footer = footer + 'Email : '+company_id.email
            
            if company_id.website:
                if footer:
                    footer = footer + ' | '
                footer = footer + 'Website : '+company_id.website
                
            
        company_formate = workbook.add_format({'font_size':10,'align':'center','valign':'vcenter', 'border':True})
        row = row+2
        sheet.merge_range(row,0,row+1,7,footer, company_formate)
        
    def set_purchase_heading(self,workbook,sheet, obj):
        po_name_formate = workbook.add_format({'bold':True,'font_size':20,'align':'center','valign':'vcenter', 'bg_color':om_bg_color,'font_color': om_font_color, 'border':True})
        if obj.state in ['draft','sent']:
            name = 'RFQ - '+ obj.name
        else:
            name = 'Purchase Order - '+ obj.name
            
        sheet.merge_range(5,0,6,7,name,po_name_formate)
    
    def set_purchase_detail(self,workbook,sheet, obj):
        partner_label_format = workbook.add_format({'bold': True, 
                                                    'font_size':10,'align':'left',
                                                    'valign':'vcenter', 
                                                    'bg_color':om_bg_color,
                                                    'font_color': om_font_color, 'border':True})
                                                    
        partner_formate = workbook.add_format({'font_size':10,'align':'left','valign':'vcenter', 'border':True})
        
        label_format = workbook.add_format({'bold': True,'font_size':10,'align':'left','valign':'vcenter','bg_color':om_bg_color,'font_color': om_font_color, 'border':True})
        val_format = workbook.add_format({'font_size':10,'align':'left','valign':'vcenter','num_format':'dd-mm-yyyy hh:mm AM/PM', 'border':True})
        partner_address = self.get_address(obj.partner_id)
        sheet.merge_range(8,0,8,2,'Vendor',partner_label_format)
        sheet.merge_range(9,0,12,2,partner_address,partner_formate)
        
        row = 9
        if obj.date_order:
            sheet.write(row,5,'Order Date',label_format)
            sheet.merge_range(row,6,row,7,obj.date_order,val_format)
            row+=1
        if obj.partner_ref:
            sheet.write(row,5,'Reference',label_format)
            sheet.merge_range(row,6,row,7,obj.partner_ref,val_format)
            row+=1
        if obj.user_id:
            sheet.write(row,5,'User',label_format)
            sheet.merge_range(row,6,row,7,obj.user_id.name,val_format)
            row+=1
    
    def set_purchase_line_details(self,workbook,sheet,obj):
        heading_format =  workbook.add_format({'bold':True,'font_size':10,'align':'left','valign':'vcenter','bg_color':om_bg_color,'font_color': om_font_color, 'border':True})
        
        c_heading_format =  workbook.add_format({'bold':True,'font_size':10,'align':'center','valign':'vcenter','bg_color':om_bg_color,'font_color': om_font_color, 'border':True})
        
        r_heading_format =  workbook.add_format({'bold':True,'font_size':10,'align':'right','valign':'vcenter','bg_color':om_bg_color,'font_color': om_font_color, 'border':True})
        
        symbol = obj.currency_id.symbol
        row = 14
        sheet.merge_range(row,0,row,2,'DESCRIPTION',heading_format)
        sheet.write(row,3,'QUANTITY',c_heading_format)
        sheet.write(row,4,'UOM',c_heading_format)
        sheet.write(row,5,'UNIT PRICE '+str(symbol),c_heading_format)
        sheet.write(row,6,'TAXES',c_heading_format)
        sheet.write(row,7,'SUB TOTAL '+str(symbol),c_heading_format)
        
        row+=1
        left_format =  workbook.add_format({'font_size':10,'align':'left', 'border':True})
        center_format =  workbook.add_format({'font_size':10,'align':'center','valign':'vcenter', 'border':True})
        center_qty_format =  workbook.add_format({'font_size':10,'align':'center','valign':'vcenter', 'border':True, 'num_format':'0.00'})
        right_format =  workbook.add_format({'font_size':10,'align':'right','valign':'vcenter', 'num_format':'0.00', 'border':True})
        for line in obj.order_line:
            sheet.merge_range(row,0,row,2,line.name or '',left_format)
            sheet.write(row,3,line.product_qty or 0.00,center_qty_format)
            sheet.write(row,4,line.product_uom.name or '',center_format)
            sheet.write(row,5,line.price_unit or 0.0,right_format)
            taxes = ', '.join(map(lambda x: (x.description or x.name), line.taxes_id))
            sheet.write(row,6,taxes or '',center_format)
            sheet.write(row,7,line.price_subtotal or 0.0,right_format)
            row+=1
        sheet.merge_range(row,0,row+1,7,'')
        
        
        row+=2
        if obj.notes:
            sheet.merge_range(row,0,row,4,'ORDER NOTES',c_heading_format)
        sheet.merge_range(row,5,row,6,'UNTAXES AMOUNT '+str(symbol),r_heading_format)
        sheet.write(row,7,obj.amount_untaxed or 0.0,right_format)
        row+=1
        if obj.notes:
            sheet.merge_range(row,0,row+1,4,obj.notes,left_format)
        sheet.merge_range(row,5,row,6,'TAX AMOUNT '+str(symbol),r_heading_format)
        sheet.write(row,7,obj.amount_tax or 0.0,right_format)
        row+=1
        sheet.merge_range(row,5,row,6,'TOTAL '+str(symbol),r_heading_format)
        sheet.write(row,7,obj.amount_total or 0.0,right_format)
        return row
        
    
    
    def generate_xlsx_report(self, workbook, data, purchases):
        company_id = self.env.user.company_id
        global om_bg_color
        om_bg_color = company_id.po_excel_bg_color
        global om_font_color
        om_font_color = company_id.po_bg_font_color
        for obj in purchases:
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.set_column('A:K', 15)
            for i in range(0,200):
                sheet.set_row(i, 20)
            self.set_company_header(workbook, sheet, obj)
            self.set_purchase_heading(workbook, sheet, obj)
            self.set_purchase_detail(workbook, sheet, obj)
            row = self.set_purchase_line_details(workbook, sheet, obj)
            self.set_company_footer(workbook, sheet, obj, row)
            
            
            
            
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
