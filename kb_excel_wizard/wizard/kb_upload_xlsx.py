from odoo import api, fields, models, _ ,exceptions
from datetime import datetime
from odoo.exceptions import Warning
import xlwt
from io import BytesIO
import base64
import binascii
import tempfile
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.tools import ustr
_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

class upload_xlsx_wizard(models.Model):
    _name = "upload_xlsx_wizard"
    _description = "Upload XLSX"

    kb_excel_file = fields.Binary(string="Select File")
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)
    kb_invoice = fields.Many2many('account.move', string="Invoices", domain=['&', '&', ('payment_state', '!=', 'paid'), ('state', '=', 'posted'), ('move_type', '=', 'out_invoice')])

    def export_template(self):
        filename = 'invoice_template.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('invoices')
        worksheet.col(0).width = 7000
        worksheet.write(0, 0, 'Invoice')
        row = 1
        for i in self.kb_invoice:
            worksheet.write(row, 0, i.name)
            row += 1
        fp = BytesIO()
        workbook.save(fp)
        var = base64.encodebytes(fp.getvalue())
        self.write({"excel_file": var, 'file_name': filename})
        fp.close()
        return {
            'name': 'invoices',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=upload_xlsx_wizard&filename_field=file_name&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename),
            'target': 'self',
        }


    def import_excel(self):
        xm = ''
        xr = []
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.kb_excel_file))
            fp.seek(0)
            # print(fp)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)

        except Exception:
            raise exceptions.ValidationError(_("Invalid file!"))
        no_invoice = 0
        no_of_row = 0
        for row_no in range(sheet.nrows):
            val = {}
            no_of_row += 1
            if row_no <= 0:
                fieldz = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))

            else:
                linez = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or ustr(row.value),
                        sheet.row(row_no)))
                account_move = self.env['account.move'].search([('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])

                to_reconcile = []

                for invoice_lines in linez:
                    for account in account_move:
                        account.invoice_outstanding_credits_debits_widget = False
                        account.invoice_has_outstanding = False
                        if invoice_lines == account.name:
                            payments = self.env['account.payment'].search([('is_reconciled', '=', False), ('partner_id', '=', account.partner_id.id)])
                            # print(payments)
                            for x in payments:
                                # print(x.line_ids)
                                for m in x.line_ids:
                                    xm = account.js_assign_outstanding_line(m.id)
                                    if not xm:
                                        xr.append(account.name)
                                    no_invoice += 1

        massage = 'Paid {} invoice(s) of {}'.format(no_invoice, no_of_row - 1)


        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': massage,
                'type': 'success',
                'sticky': True,
            }
        }

