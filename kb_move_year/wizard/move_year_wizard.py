from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf
import binascii
import tempfile
from tempfile import TemporaryFile
from odoo.tools import ustr
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

class MoveYearWizard(models.TransientModel):
    _name = 'move.year.wizard'

    kb_academic_year_id_from = fields.Many2one(comodel_name="academic_year", string="Current Year")
    kb_academic_year_id_to = fields.Many2one(comodel_name="academic_year", string="Next Year")

    kb_current_standard = fields.Many2one(comodel_name="grade", string="Current Class")
    kb_move_standard = fields.Many2one(comodel_name="grade", string="Move to")
   
    kb_excel_file = fields.Binary(string="Select File")
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

    def move_student(self):
        # raise exceptions.ValidationError(_(tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")))

        # try:
        #     fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xls")
        #     fp.write(binascii.a2b_base64(self.kb_excel_file))
        #     fp.seek(0)
        #     values = {}
        #     workbook = xlrd.open_workbook(fp.name)
        #     sheet = workbook.sheet_by_index(0)
        # except Exception:
        #     raise exceptions.ValidationError(_("Invalid file!"))

        no_stu = 0
        no_of_row = 0
        done_stu = 0
        alumni = 0
        # xr = []
        # for row_no in range(sheet.nrows):
        #     if row_no >= 1:
        #         row_vals = sheet.row_values(row_no)
        student_id15 = self.env['student'].search([('academic_year', '=', self.kb_academic_year_id_from.id),('grades.id', '=', 15)])
        student_idsa = self.env['student'].search([('academic_year', '=', self.kb_academic_year_id_from.id)])
        # print()
        # look to this for 
        # for x in student_id15:
        #     if x.standard_id.standard_id.id == 15:
        #         x.standard_id = False
        #         x.set_alumni()
        #         alumni += 1
        
        
        for stu in student_idsa:
            no_stu += 1
            if stu.grades.id == self.kb_current_standard.id:
                stu.academic_year = self.kb_academic_year_id_to.id
                stu.grades = self.kb_move_standard.id
                done_stu += 1
                

                
              
                
                    
        
        massage = 'Move {} student(s) of {} and {} are alumni'.format(done_stu, no_stu, alumni)
        print(massage)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': massage,
                'type': 'success',
                'sticky': True,
            }
        }
    

    def print_excel_report(self):
        filename = 'Classes.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('classes')

        # date_from = self.date_from
        # date_to = self.date_to
        standard_ids = self.env['standard.division'].search([],order="name asc")
            

        

        worksheet.col(0).width = 10000
        worksheet.col(0).length = 3000
        worksheet.col(1).width = 10000
        worksheet.col(2).width = 4000
        worksheet.col(3).width = 7000
        worksheet.col(4).width = 7000
        worksheet.col(5).width = 7000
        worksheet.col(6).width = 6000
        worksheet.col(7).width = 7000
        worksheet.col(8).width = 7000

        bold = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
        style = xlwt.easyxf(' align: wrap on, vert centre, horiz center', )
        style0 = xlwt.easyxf('align: wrap on, vert centre, horiz center',
                                num_format_str='#,##0.00')
        style_total = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center',
                                    num_format_str='#,##0.00')
        style1 = xlwt.easyxf('align: wrap on, vert centre, horiz center', num_format_str='YYYY')
        style2 = xlwt.easyxf('align: wrap on, vert centre, horiz center', num_format_str='DD-MMM-YYYY')

        worksheet.write(0, 0, 'Current Class', bold)
        worksheet.write(0, 1, 'Move To', bold)

        row = 0
        col = 0
        total_residual_value = 0
        total_depreciation = 0
        total_gross = 0
        acc_total = 0
        code = 0

        # rsv =  total2 - residual_value

        for y in standard_ids:


            row += 1
            code += 1
            worksheet.write(row, col, y.name, style)
            worksheeines = []
        

        fp = BytesIO()
        workbook.save(fp)
        var = base64.encodebytes(fp.getvalue())
        self.write({"excel_file": var, 'file_name': filename})
        fp.close()
        return {
            'name': 'Move Year',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=move.year.wizard&filename_field=file_name&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename),
            'target': 'self',
        }