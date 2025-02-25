from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import xlwt


class kb_draft_salary_report_wizard(models.TransientModel):
    _name = "kb_draft_salary_report_wizard"
    _description = "draft salary report"
    kb_search_employee = fields.Selection([
        ('selection1', "All employee"),
        ('selection2', "Specific employee")
    ], string='Employee', default='selection1')

    kb_name_employee = fields.Many2one('hr.employee', "Employee name")
    kb_date_start = fields.Date(string='Date To' , required=True)
    kb_date_end = fields.Date(string='Date From', required=True)
    kb_country_id = fields.Many2one('res.country', string='Nationality (Country)')

    def action_print_document_pdf(self):
        for rec in self :
            employee_salaries = []
            report_information=[]
            domain = []
            BASIC = 0.0
            HRA= 0.0
            DA=0.0
            Other=0.0
            Travel=0.0
            NET = 0.0
            LO = 0.0
            INSUR=0.0
            Punishments=0.0
            data = {
                'form_data': self.read()[0],
                'employees': employee_salaries,
                'information': report_information
            }
            number_day=0.0
            domain += [('state', '=', 'draft')]
            if rec.kb_name_employee:
                domain += [('employee_id', '=', rec.kb_name_employee.id)]

            if rec.kb_date_start:
                domain += [('date_from', '>=', rec.kb_date_start)]

            if rec.kb_date_end:
                domain += [('date_to', '<=', rec.kb_date_end)]

            if rec.kb_country_id:
                domain += [('employee_id.country_id', '=', rec.kb_country_id.id)]


            if domain:
                kb_payslips = self.env['hr.payslip'].search(domain)
            else:
                kb_payslips = self.env['hr.payslip'].search([])

            if rec.kb_date_start:
                kb_start = self.kb_date_start.month
                kb_start_year = self.kb_date_start.year
            if rec.kb_date_end:
                kb_end = self.kb_date_end.month
            if kb_start == kb_end:
                month = self.kb_date_start.strftime('%B')
                date= str(kb_start)+'/'+ str(kb_start_year)
                if rec.kb_country_id:
                    report_information.append({
                        'company':self.env.company.name,
                       'month':month,
                       'dates':date,
                        'all':'الجميع',
                        'kb_country_id':rec.kb_country_id.name
                    })
                else:
                    report_information.append({
                        'company': self.env.company.name,
                        'month': month,
                        'dates': date,
                        'all': 'الجميع',
                        'kb_country_id': 'الجميع',
                    })


                for payslip in kb_payslips:
                    employee_name = payslip.employee_id.name
                    employee_id = payslip.employee_id.id
                    employee_job_title = payslip.employee_id.job_title
                    if payslip.worked_days_line_ids:
                        number_day=payslip.worked_days_line_ids[0].number_of_days
                    if kb_start <= payslip.date_from.month <= kb_end:
                        if employee_name not in employee_salaries:
                            for payslip_line in payslip.line_ids:
                                if payslip_line.code == 'BASIC':
                                    BASIC = payslip_line.amount
                                if payslip_line.code == 'HRA':
                                    HRA = payslip_line.amount
                                if payslip_line.code == 'DA':
                                    DA = payslip_line.amount
                                if payslip_line.code == 'Travel':
                                    Travel = payslip_line.amount
                                if payslip_line.code == 'Other':
                                    Other = payslip_line.amount
                                if payslip_line.code == 'NET':
                                    NET = payslip_line.amount
                                if payslip_line.code == 'LO':
                                    LO = payslip_line.amount
                                if payslip_line.code == 'INSUR':
                                    INSUR = payslip_line.amount
                            total_deduction= LO + INSUR +Punishments
                            total_salary= NET - total_deduction
                            employee_salaries.append({
                                'employee_id':employee_id,
                                'employee_name':employee_name,
                                'employee_job_title':employee_job_title,
                                'number_day':number_day,
                                'BASIC': BASIC,
                                'HRA': HRA,
                                'Travel': Travel,
                                'Other': Other,
                                'DA': DA,
                                'NET': NET,
                                'LO': LO,
                                'INSUR': INSUR,
                                'Punishments': Punishments,
                                'total_deduction': total_deduction,
                                'total_salary': total_salary,
                            })
            else:
                raise ValidationError(_('The start date and end date must in same month'))
            # raise ValidationError(_(employee_salaries[0]['employee_id']))

            return self.env.ref('kb_salary_print_draft.kb_draft_salary_report_wizard').report_action(self,data=data)

    def action_print_document_xlsx(self):
        for rec in self:
            employee_salaries = []
            report_information = []
            domain = []
            BASIC = 0.0
            HRA = 0.0
            DA = 0.0
            Other = 0.0
            Travel = 0.0
            NET = 0.0
            LO = 0.0
            INSUR = 0.0
            Punishments = 0.0
            data = {
                'form_data': self.read()[0],
                'employees': employee_salaries,
                'information': report_information
            }
            number_day = 0.0
            domain += [('state', '=', 'draft')]
            if rec.kb_name_employee:
                domain += [('employee_id', '=', rec.kb_name_employee.id)]

            if rec.kb_date_start:
                domain += [('date_from', '>=', rec.kb_date_start)]

            if rec.kb_date_end:
                domain += [('date_to', '<=', rec.kb_date_end)]

            if rec.kb_country_id:
                domain += [('employee_id.country_id', '=', rec.kb_country_id.id)]

            if domain:
                kb_payslips = self.env['hr.payslip'].search(domain)
            else:
                kb_payslips = self.env['hr.payslip'].search([])

            if rec.kb_date_start:
                kb_start = self.kb_date_start.month
                kb_start_year = self.kb_date_start.year
            if rec.kb_date_end:
                kb_end = self.kb_date_end.month
            if kb_start == kb_end:
                month = self.kb_date_start.strftime('%B')
                date = str(kb_start) + '/' + str(kb_start_year)
                if rec.kb_country_id:
                    report_information.append({
                        'company': self.env.company.name,
                        'month': month,
                        'dates': date,
                        'all': 'الجميع',
                        'kb_country_id': rec.kb_country_id.name
                    })
                else:
                    report_information.append({
                        'company': self.env.company.name,
                        'month': month,
                        'dates': date,
                        'all': 'الجميع',
                        'kb_country_id': 'الجميع',
                    })

                for payslip in kb_payslips:
                    employee_name = payslip.employee_id.name
                    employee_id = payslip.employee_id.id
                    employee_job_title = payslip.employee_id.job_title
                    if payslip.worked_days_line_ids:
                        number_day = payslip.worked_days_line_ids[0].number_of_days
                    if kb_start <= payslip.date_from.month <= kb_end:
                        if employee_name not in employee_salaries:
                            for payslip_line in payslip.line_ids:
                                if payslip_line.code == 'BASIC':
                                    BASIC = payslip_line.amount
                                if payslip_line.code == 'HRA':
                                    HRA = payslip_line.amount
                                if payslip_line.code == 'DA':
                                    DA = payslip_line.amount
                                if payslip_line.code == 'Travel':
                                    Travel = payslip_line.amounti
                                if payslip_line.code == 'Other':
                                    Other = payslip_line.amount
                                if payslip_line.code == 'NET':
                                    NET = payslip_line.amount
                                if payslip_line.code == 'LO':
                                    LO = payslip_line.amount
                                if payslip_line.code == 'INSUR':
                                    INSUR = payslip_line.amount
                            total_deduction = LO + INSUR + Punishments
                            total_salary = NET - total_deduction
                            employee_salaries.append({
                                'employee_id': employee_id,
                                'employee_name': employee_name,
                                'employee_job_title': employee_job_title,
                                'number_day': number_day,
                                'BASIC': BASIC,
                                'HRA': HRA,
                                'Travel': Travel,
                                'Other': Other,
                                'DA': DA,
                                'NET': NET,
                                'LO': LO,
                                'INSUR': INSUR,
                                'Punishments': Punishments,
                                'total_deduction': total_deduction,
                                'total_salary': total_salary,
                            })
            else:
                raise ValidationError(_('The start date and end date must in same month'))
        return self.env.ref('kb_salary_print_draft.kb_draft_salary_excel_action').report_action(self,data=data)

class kb_draft_salary_details_excel(models.AbstractModel):
    _name = "report.kb_salary_print_draft.kb_draft_salary_excel_action"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, contract):
        sheet = workbook.add_worksheet('كشف رواتب لشهر')
        bold = workbook.add_format({'bold': True})
        # title_style = xlwt.easyxf('font: bold on, color black;\
        #                             borders: top_color black, bottom_color black, right_color black, left_color black,\
        #                                      left     thin     , right thin, top thin, bottom thin;\
        #                                      pattern: pattern   solid, fore_color white;\
        #                                      align  : horiz     center;\
        #                                      font   : height    280,')

        row = 0
        col = 0
        count=0
        for information in data['information']:
            sheet.merge_range(row, col+11, row, col+12, str(information['dates'])+'كشف رواتب لشهر', bold)

            sheet.write(row +2, col + 5,  information['company'])
            sheet.write(row+2, col + 6, 'الفرع', bold)

            sheet.write(row +2, col + 19,  information['dates']+'كشف رواتب لشهر')
            sheet.write(row+2, col + 20, 'التقرير', bold)

            sheet.write(row + 3, col + 19, information['month'])
            sheet.write(row + 3, col + 20, 'الشهر', bold)

            sheet.write(row+3, col + 6, 'القسم', bold)

            sheet.write(row +4, col + 19,  information['all'])
            sheet.write(row+4, col + 20, 'طرق الدفع', bold)

            sheet.write(row +5, col + 5,  information['all'])
            sheet.write(row+5, col + 6, 'حالة الكشف', bold)

            sheet.write(row +5, col + 19,  information['all'])
            sheet.write(row+5, col + 20, 'صندوق التنمية', bold)

            sheet.write(row + 6, col + 5, information['kb_country_id'])
            sheet.write(row + 6, col + 6, 'الجنسية', bold)

            sheet.write(row +6, col + 19,  information['all'])
            sheet.write(row+6, col + 20, 'ملف مكتب العمل ', bold)

        # row_employee=9
        sheet.write(row + 9 , col + 5, 'الصافي', bold)
        sheet.write(row + 9, col + 6, 'مجموع الاقتطاعات ', bold)
        sheet.write(row + 9, col + 7, 'عقوبات و جزاءات ', bold)
        sheet.write(row + 9, col + 8, 'سلفة ', bold)
        sheet.write(row + 9, col + 9, 'التأمينات الاجتماعية ', bold)
        sheet.write(row + 9, col + 10, 'اجمالي الراتب المستحق ', bold)
        sheet.write(row + 9, col + 11, 'بدلات إعاشه ', bold)
        sheet.write(row + 9, col + 12, 'بدلات اخرى ', bold)
        sheet.write(row + 9, col + 13, 'بدل نقل ', bold)
        sheet.write(row + 9, col + 14, 'بدل سكن ', bold)
        sheet.write(row + 9, col + 15, 'الراتب الاساسي', bold)
        sheet.write(row + 9, col + 16, 'ايام الدوام', bold)
        sheet.write(row + 9, col + 17, 'المنصب', bold)
        sheet.write(row + 9, col + 18, 'الموظف', bold)
        sheet.write(row + 9, col + 19, 'رقم الموظف', bold)
        sheet.write(row + 9, col + 20, 'رقم', bold)

        for Employees in data['employees']:
            count+=1
            row += 1
            sheet.write(row + 9, col +5, Employees['total_salary'])
            sheet.write(row + 9, col + 6, Employees['total_deduction'])
            sheet.write(row + 9, col + 7, Employees['Punishments'])
            sheet.write(row + 9, col + 8, Employees['INSUR'])
            sheet.write(row + 9, col + 9, Employees['LO'])
            sheet.write(row + 9, col + 10, Employees['NET'])
            sheet.write(row + 9, col + 11, Employees['DA'])
            sheet.write(row + 9, col + 12, Employees['Other'])
            sheet.write(row + 9, col + 13, Employees['Travel'])
            sheet.write(row + 9, col + 14, Employees['HRA'])
            sheet.write(row + 9, col + 15, Employees['BASIC'])
            sheet.write(row + 9, col + 16, Employees['number_day'])
            sheet.write(row + 9, col + 17, Employees['employee_job_title'])
            sheet.write(row + 9, col + 18, Employees['employee_name'])
            sheet.write(row + 9, col + 19, Employees['employee_id'])
            sheet.write(row + 9, col + 20, count)
