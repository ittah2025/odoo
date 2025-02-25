from odoo import models, _
import xlsxwriter
from odoo.exceptions import ValidationError

class report_xslx(models.AbstractModel):

    _name = "report.kb_daily_sales_report.report_xslx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Summary XLSX Report"

    def generate_xlsx_report(self, workbook, data, account_move):
        sheet = workbook.add_worksheet ('Invoice Details')
        sheet2 = workbook.add_worksheet ('Payment Details')
        sheet3 = workbook.add_worksheet ('Total Details')
        bold = workbook.add_format({'bold': True})
        
        # Invoice details
        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 11)

        row = 1
        col = 1

        sheet.write(row, col,'Total',bold)
        sheet.write(row, col + 1,'Sale Man',bold)
        sheet.write(row, col + 2, 'Sale Order',bold)
        sheet.write(row, col + 3,'Journal Code',bold)
        sheet.write(row, col + 4,'Inovice Date',bold)
        sheet.write(row, col + 5,'Customer',bold)
        # sheet.write(row, col + 6,'Branch',bold)
        sheet.write(row, col + 7,'Refrence',bold)

        total =0
        invoice_total= 0
        for move in data['move_ids']:
            # raise ValidationError(_(move))
            row += 1
            sheet.write(row, col, move['amount_total'])
            sheet.write(row, col + 1, move['invoice_user_id'][1])
            sheet.write(row, col + 2, '')
            sheet.write(row, col + 3, move['name'])
            sheet.write(row, col + 4, move['date'])
            sheet.write(row, col + 5, move['partner_id'][1])
            # sheet.write(row, col + 6, move['branch_id'][1])
            sheet.write(row, col + 6, move['name'])
            if move['name'][0] == 'R':
                invoice_total += move['amount_total']
            else:
                total += move['amount_total']

            # sheet.write(row, col + 7, move['amount_total_signed']['total'])
        
        # Payment details
        sheet2.set_column('D:D', 10)
        sheet2.set_column('E:E', 11)

        roww = 1
        coll = 1

        
        sheet2.write(roww, coll,'Total',bold)
        sheet2.write(roww, coll + 1,'Sale Man',bold)
        sheet2.write(roww, coll + 2, 'Invoice Number',bold)
        sheet2.write(roww, coll + 3,'Journal Code',bold)
        sheet2.write(roww, coll + 4,'Payment Date',bold)
        sheet2.write(roww, coll + 5,'Customer',bold)
        # sheet2.write(roww, coll + 6,'Branch',bold)
        sheet2.write(roww, coll + 6,'Refrence',bold)
        
        for payments in data['payment_ids']:
            roww += 1
            sheet2.write(roww, coll, payments['amount_total'])
            sheet2.write(roww, coll + 1, payments['user_id'][1])
            sheet2.write(roww, coll + 2, payments['name'])
            sheet2.write(roww, coll + 3, payments['journal_id'][1])
            sheet2.write(roww, coll + 4, payments['date'])
            sheet2.write(roww, coll + 5, payments['partner_id'][1])
            # sheet2.write(roww, coll + 6, payments['branch_id'][1])
            sheet2.write(roww, coll + 6,  payments['ref'])

        sheet3.set_column('D:D', 10)
        sheet3.set_column('E:E', 11)

        rowww = 0
        colll = 0

        sheet3.write(rowww, colll,'Invoice Total',bold)
        sheet3.write(rowww+1, colll, invoice_total)
        sheet3.write(rowww, colll+1, 'Bank',bold)
        sheet3.write(rowww+1, colll+1, total - invoice_total)
        sheet3.write(rowww, colll+2, 'Total',bold)
        sheet3.write(rowww+1, colll+2,  total+invoice_total)