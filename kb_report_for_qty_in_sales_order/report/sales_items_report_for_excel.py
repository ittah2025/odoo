# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalItemsReport(models.AbstractModel):
    _name = 'report.kb_report_for_qty_in_sales_order.sale_report'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, product_ids):
        # style
        sheet = workbook.add_worksheet('Products QTY Report')
        # bold0 = workbook.add_format({"bold": True})
        heading = workbook.add_format({"font_size": 14,'num_format': 'yyyy-mm-dd','left': True,'valign': 'center', 'bold': True, 'bg_color': '#fffbed', })
        date_style = workbook.add_format({'num_format': 'yyyy-mm-dd','left': True,'valign': 'left', 'bold': True, 'bg_color': '#fffbed', })
        center_style = workbook.add_format({'valign': 'center', 'bold': True, 'bg_color': '#fffbed', })
        title_center_style = workbook.add_format({'valign': 'center', 'bold': True, 'bg_color': '#f2eee4', })
        # wrap_text = workbook.add_format({'text_wrap': True, 'bg_color': '#FFFFFFF'})
        # money = workbook.add_format({'num_format': '$#,##0.00', 'bg_color': '#ffffff'})
        # white_bg = workbook.add_format({'bg_color': 'white'})
        # bottom_border = workbook.add_format({'bottom': True})
        # left_border = workbook.add_format({'left': True,'valign': 'left', 'bold': True, 'bg_color': '#fffbed', })
        # title_left_border = workbook.add_format({'left': True,'valign': 'left', 'bold': True, 'bg_color': '#f2eee4', })
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#FFFF00', 'border': True})
        title = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 17, 'bg_color': '#eae5db', 'border': True})
        sub_title = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 13, 'bg_color': '#eae5db', 'border': True})
        row = 4
        col = 0
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 4, 40)
        sheet.set_column(5, 5, 20)
        sheet.set_row(row, 20)
        # sheet.right_to_left()
        sheet.merge_range('A1:F2', 'Products QTY Report ( From %s To %s ) ' % (data['form']['date_from'], data['form']['date_to']), title)
        # sheet.merge_range('A1:F2', 'Account Name', center_style)
        # sheet.merge_range('A1:F2', 'Debit', center_style)
        # sheet.merge_range('A1:F2', 'Credit', center_style)
        domain = []
        done_append_ids = []
        product_returns_data = []
        list_data = []
        if data['form']['product_ids']:
            # print('account_ids=======', data['form']['product_ids'])
            for p in data['form']['product_ids']:
                # print('ppppppp==', p)
                all_pro = self.env['product.template'].search([('id', '=', p)])
                total_qty = 0
                for l in all_pro:
                    pro_qty = self.env['sale.order.line'].search([('product_template_id', '=', l.id)])
                    for r in pro_qty:
                        custom_date = r.order_id.date_order.date()
                        if data['form']['date_to'] >= str(custom_date) >= data['form']['date_from']:
                            total_qty += r.product_uom_qty
                    if total_qty > 0:
                        list_data.append(
                            {
                                'name': l.name,
                                'total_qty': total_qty,
                            }
                        )
                    # print('fooor total_lines==', total_data)
            sheet.set_row(row, 20)
            sheet.write(row, 0, 'Product Name', heading)
            sheet.write(row, 1, 'Total QTY', heading)
            # sheet.write(row, 2, 'Total Credit', heading)
            # sheet.write(row, 3, 'End Balance Debit', heading)
            # sheet.write(row, 4, 'End Balance Credit', heading)
            # print('list_data==', list_data)
            for pr in list_data:
                sheet.set_row(row, 20)
                row += 2
                # sheet.merge_range(row, col, row, col + 5, pr['account_name'], title)
                sheet.write(row, 0, pr['name'], center_style)
                sheet.write(row, 1, pr['total_qty'], center_style)
                sheet.set_row(row, 20)
            row += 2

        else:
            all_pro = self.env['product.template'].search([])
            for p in all_pro:
                all_pro = self.env['product.template'].search([('id', '=', p)])
                total_qty = 0
                for l in all_pro:
                    pro_qty = self.env['sale.order.line'].search([('product_template_id', '=', l.id)])
                    for r in pro_qty:
                        custom_date = r.order_id.date_order.date()
                        if data['form']['date_to'] >= str(custom_date) >= data['form']['date_from']:
                            total_qty += r.product_uom_qty
                    if total_qty > 0:
                        list_data.append(
                            {
                                'name': l.name,
                                'total_qty': total_qty,
                            }
                        )
            sheet.set_row(row, 20)
            sheet.write(row, 0, 'Product Name', heading)
            sheet.write(row, 1, 'Total QTY', heading)
            unique_products = []
            # print('list_data==', list_data)
            for pr in list_data:
                sheet.set_row(row, 20)
                row += 2
                sheet.write(row, 0, pr['name'], center_style)
                sheet.write(row, 1, pr['total_qty'], center_style)
                sheet.set_row(row, 20)
            row += 2