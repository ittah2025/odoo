from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf


class KbAlrajhiSalary(models.TransientModel):
    _name = 'rajhi_salary'

    kb_definition_type = fields.Selection([
        ('rajhi_salary', 'Al Rajhi Salary Definition'),
        ('fix_salary', 'Fixing Salary'),
        ('employee_salary', 'Employees Salaries'),

    ], string="Document Type")

    kb_sign_employee = fields.Many2one('hr.employee', string="Name of the authorized signatory")

    employee_id = fields.Many2one('hr.employee', string="Employee name")

    kb_end_of_service = fields.Char(string="End of service benefits")
    kb_end_of_service_terminate = fields.Char(string="End of service benefits before the end of contract")

    def print_wizard_pdf(self):
        employee_ids = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        salary_ids_list = []
        for i in employee_ids:
            for x in i.contract_ids:
                vals = {
                    'name': i.name,
                    'nationality': i.country_id.name,
                    'identification_id': i.identification_id,
                    'barcode': i.barcode,
                    'job_id': i.job_id.name,
                    'first_contract_date': i.first_contract_date,
                    'bank_account_id': i.bank_iban_number,
                    'bank_account_name': i.bank_name,
                    'total_wage': x.wage + x.hra + x.da + x.travel_allowance + x.fixed_allowance + x.unfixed_allowance + x.working_other_companies_allowance + x.meal_allowance + x.medical_allowance + x.other_allowance,
                    'wage': x.wage,
                    'hra': x.hra,
                    'da': x.da,
                    'travel_allowance': x.travel_allowance,
                    'fixed_allowance': x.fixed_allowance,
                    'unfixed_allowance': x.unfixed_allowance,
                    'working_other_companies_allowance': x.working_other_companies_allowance,
                    'meal_allowance': x.meal_allowance,
                    'medical_allowance': x.medical_allowance,
                    'other_allowance': x.other_allowance,
                    'currency_id': x.currency_id.id,
                    'kb_sign_employee': self.kb_sign_employee.name,
                    'kb_end_of_service': self.kb_end_of_service,
                    'kb_end_of_service_terminate': self.kb_end_of_service_terminate,
                }
                salary_ids_list.append(vals)

                data = {
                    'form_data': self.read()[0],
                    'salary_list_loop': salary_ids_list,
                    'result_ids': [],

                }

                return self.env.ref('kb_alrajhi_wizard.salary_rajhi_report_print').report_action(self, data=data)

    excel_file = fields.Binary('Excel Report Salaries')
    file_name = fields.Char('Excel File', size=64)

    def print_wizard_excel(self):
        all_employee_ids = self.env['hr.employee'].search([])

        all_salary_ids_list = []

        for i in all_employee_ids:
            for x in i.contract_ids:
                all_payroll = self.env['hr.payslip'].search([('employee_id', '=', i.id)])
                deduction = 0.0
                basic_salary = 0.0
                net_salary = 0.0
                hra_salary = 0.0
                other_salary = 0.0
                for y in all_payroll.line_ids:

                    if y.category_id.code == "BASIC":
                        basic_salary = y.total

                    if y.category_id.code == "DED":
                        deduction = y.total

                    if y.category_id.code == "NET":
                        net_salary = y.total

                    if y.category_id.code == "HRA":
                        hra_salary = y.total

                    if y.category_id.code == "Other":
                        other_salary = y.total

                vals = {
                    'name': i.name,
                    'nationality': i.country_id.name,
                    'identification_id': i.identification_id,
                    'barcode': i.barcode,
                    'job_id': i.job_id.name,
                    'first_contract_date': i.first_contract_date,
                    'bank_account_id': i.bank_iban_number,
                    'bank_account_name': i.bank_name,
                    'total_wage': x.wage + x.hra + x.da + x.travel_allowance + x.fixed_allowance + x.unfixed_allowance + x.working_other_companies_allowance + x.meal_allowance + x.medical_allowance + x.other_allowance,
                    'wage': x.wage,
                    'hra': x.hra,
                    'da': x.da,
                    'travel_allowance': x.travel_allowance,
                    'fixed_allowance': x.fixed_allowance,
                    'unfixed_allowance': x.unfixed_allowance,
                    'working_other_companies_allowance': x.working_other_companies_allowance,
                    'meal_allowance': x.meal_allowance,
                    'medical_allowance': x.medical_allowance,
                    'other_allowance': x.other_allowance,
                    'currency_id': x.currency_id.id,
                    'kb_sign_employee': self.kb_sign_employee.name,
                    'kb_end_of_service': self.kb_end_of_service,
                    'kb_end_of_service_terminate': self.kb_end_of_service_terminate,
                    'deduction': deduction,
                    'basic_salary': basic_salary,
                    'net_salary': net_salary,
                    'hra_salary': hra_salary,
                    'other_salary': other_salary,
                }
                all_salary_ids_list.append(vals)
        bold = xlwt.easyxf('font: bold on, color white;\
                                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left    thin, right thin, top thin, bottom thin;\
                                              pattern: pattern solid, fore_color dark_blue_ega;\
                                              align  : horiz center,')

        bold_total = xlwt.easyxf('font: bold on, color black;\
                                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left    thin, right thin, top thin, bottom thin;\
                                              pattern: pattern solid, fore_color gray25;\
                                              align  : horiz center',
                                 num_format_str='#,##0.00')

        style = xlwt.easyxf(' align: wrap on, vert centre, horiz center', )
        style0 = xlwt.easyxf('align: wrap on, vert centre, horiz center',
                             num_format_str='#,##0.00')
        style_total = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center',
                                  num_format_str='#,##0.00')
        style1 = xlwt.easyxf('align: wrap on, vert centre, horiz center', num_format_str='YYYY')
        style2 = xlwt.easyxf('align: wrap on, vert centre, horiz center', num_format_str='DD-MMM-YYYY')

        title_style = xlwt.easyxf('font: bold on, color black;\
                                             borders: top_color black, bottom_color black, right_color black, left_color black,\
                                                      left     thin     , right thin, top thin, bottom thin;\
                                                      pattern: pattern   solid, fore_color white;\
                                                      align  : horiz     center;\
                                                      font   : height    280,')

        filename = 'employee_salary.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('sheet 1')

        worksheet.col(0).width = 7000
        worksheet.row(4).height = 580
        worksheet.col(1).width = 7000
        worksheet.col(2).width = 7000
        worksheet.col(3).width = 7000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000
        worksheet.col(6).width = 5000
        worksheet.col(7).width = 5000
        worksheet.col(8).width = 5000
        worksheet.col(9).width = 5000
        worksheet.col(10).width = 5000
        worksheet.col(11).width = 5000
        worksheet.col(12).width = 5000
        worksheet.col(13).width = 5000
        worksheet.col(14).width = 5000
        worksheet.col(15).width = 5000
        worksheet.col(16).width = 7000
        worksheet.col(17).width = 7000
        worksheet.col(18).width = 7000

        worksheet.write(4, 0, "Bank Name \n اسم البنك", bold)
        worksheet.write(4, 1, "Account Number \n رقم الحساب", bold)
        worksheet.write(4, 2, "Employee Name \n اسم الموظف", bold)
        worksheet.write(4, 3, "Employee Number \n الرقم الوظيفي", bold)
        worksheet.write(4, 4, "National ID \n رقم الهوية ", bold)
        worksheet.write(4, 5, "Salary \n الراتب ", bold)
        worksheet.write(4, 6, "Basic Salary \n الراتب الاساسي", bold)
        worksheet.write(4, 7, "Housing Allowance \n بدل سكن", bold)
        # worksheet.write(4, 8, "Dearness Allowance \n بدل غربة", bold)
        # worksheet.write(4, 9, "Travel Allowance \n بدل مواصلات", bold)
        # worksheet.write(4, 10, "Fixed Allowance \n بدل ثابت", bold)
        # worksheet.write(4, 11, "Unfixed Allowance\n بدل غير ثابت", bold)
        # worksheet.write(4, 12, "Working In Other Companies Allowance \n بدل العمل في شركات أخرى", bold)
        # worksheet.write(4, 13, "Meal Allowance \n بدل الوجبات", bold)
        # worksheet.write(4, 14, "Medical Allowance \n بدلات طبية", bold)
        worksheet.write(4, 8, "Other Allowance \n بدلات اخرى", bold)
        worksheet.write(4, 9, "Deductions \n الخصومات", bold)
        worksheet.write(4, 10, "Employee Remarks \n ملاحظات الموظف", bold)
        worksheet.write(4, 11, "Employee Department \n قصم الموظف", bold)

        row = 5

        for w in all_salary_ids_list:
            worksheet.write(row, 0, w['bank_account_name'], style)
            worksheet.write(row, 1, w['bank_account_id'], style)
            worksheet.write(row, 2, w['name'], style2)
            worksheet.write(row, 3, w['barcode'], style)
            worksheet.write(row, 4, w['identification_id'], style)
            worksheet.write(row, 5, w['net_salary'], style)
            worksheet.write(row, 6, w['basic_salary'], style)
            worksheet.write(row, 7, w['hra_salary'], style)
            # worksheet.write(row, 8, w['da'], style)
            # worksheet.write(row, 9, w['travel_allowance'], style)
            # worksheet.write(row, 10, w['fixed_allowance'], style)
            # worksheet.write(row, 11, w['unfixed_allowance'], style)
            # worksheet.write(row, 12, w['working_other_companies_allowance'], style)
            # worksheet.write(row, 13, w['meal_allowance'], style)
            # worksheet.write(row, 14, w['medical_allowance'], style)
            worksheet.write(row, 8, w['other_salary'], style)
            worksheet.write(row, 9, w['deduction'], style)
            worksheet.write(row, 10, '', style)
            worksheet.write(row, 11, w['job_id'], style)
            row += 1

        fp = BytesIO()
        workbook.save(fp)
        var = base64.encodebytes(fp.getvalue())
        self.write({"excel_file": var, 'file_name': filename})
        fp.close()
        return {
            'name': 'Salaries Report',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=rajhi_salary&filename_field=file_name&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename),
            'target': 'self',
        }
