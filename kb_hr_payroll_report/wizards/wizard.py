# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import itertools
from operator import itemgetter
import operator
from datetime import datetime
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf


class KBPayrollStatementWizard(models.TransientModel):
    _name = 'payroll.statement.wizard'

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    statement_by = fields.Selection([('batch', 'Payslip Batch'),
                                     ('date', 'Date')], default='date', required=1)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id)
    employee_ids = fields.Many2many("hr.employee", string="Employee")
    group_by = fields.Selection([('month', 'Month'),
                                 ('employee', 'Employee'),
                                 ('department', 'Department')])
    batch_payslip_id = fields.Many2one('hr.payslip.run', string='Batch Payslip')
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

    def get_payslip(self):
        if self.statement_by == 'date':
            sql_query = """select ps.id from hr_payslip as ps left join hr_employee as emp on ps.employee_id = emp.id where ps.company_id = %s and ps.employee_id in %s and ps.date_from >= %s and ps.date_to <= %s"""
            params = (self.company_id.id, tuple(self.employee_ids.ids), self.date_from, self.date_to)
            self.env.cr.execute(sql_query, params)
            results = self.env.cr.dictfetchall()
            payslip_ids = [payslip.get('id') for payslip in results]
        else:
            payslip_ids = [slip.id for slip in self.batch_payslip_id.slip_ids]
        return payslip_ids

    def print_pdf(self):
        if not self.employee_ids and self.statement_by == 'date':
            raise ValidationError(_('Please Select Employee !!!'))

        payslip_ids = self.get_payslip()
        if not payslip_ids:
            raise ValidationError(_('Payslip not found !!!'))
        return self.env.ref('kb_hr_payroll_report.print_payroll_statement').report_action(self, data=None)

    def get_code_list(self,payslip_ids):
        sql_query = """select psl.salary_rule_id as rule_id from hr_payslip_line as psl join hr_payslip as ps on ps.id = psl.slip_id join hr_salary_rule as salaryrule on psl.salary_rule_id = salaryrule.id  where ps.id in %s and salaryrule.appears_on_payslip = 't'"""
        params = (tuple(payslip_ids),)
        self.env.cr.execute(sql_query, params)
        results = self.env.cr.dictfetchall()
        rule_lst = [line.get('rule_id') for line in results]
        rule_ids = self.env['hr.salary.rule'].search([('id','in',rule_lst)],order='sequence')
        lst = []
        for rule in rule_ids:
            lst.append(rule.code)
        return lst

    def get_lines(self, payslip_ids, code_list):
        lines = []
        for payslip in self.env['hr.payslip'].browse(payslip_ids):
            payslip_date = datetime.strptime(str(payslip.date_from), '%Y-%m-%d')
            month = payslip_date.strftime("%B")
            line_val = self.get_line_val(payslip, code_list)
            dic = {
                'month': month,
                'employee': payslip.employee_id and payslip.employee_id.name or '',
                'ID': payslip.employee_id and payslip.employee_id.identification_id or '',
                'department': payslip.employee_id and payslip.employee_id.department_id and payslip.employee_id.department_id.name or '',
                'lines': line_val,
            }
            lines.append(dic)

        if self.group_by == 'month':
            n_lines = sorted(lines, key=itemgetter('month'))
            groups = itertools.groupby(n_lines, key=operator.itemgetter('month'))
            lines = [{'month': k, 'values': [x for x in v]} for k, v in groups]
        elif self.group_by == 'employee':
            n_lines = sorted(lines, key=itemgetter('employee'))
            groups = itertools.groupby(n_lines, key=operator.itemgetter('employee'))
            lines = [{'month': k, 'values': [x for x in v]} for k, v in groups]
        elif self.group_by == 'department':
            n_lines = sorted(lines, key=itemgetter('department'))
            groups = itertools.groupby(n_lines, key=operator.itemgetter('department'))
            lines = [{'month': k, 'values': [x for x in v]} for k, v in groups]

        return lines

    def get_line_val(self,payslip,code_list):
        val_lst=[]
        for code in code_list:
            val=self.get_payslip_line_val(payslip,code)
            val_lst.append(val)
        return val_lst

    def get_payslip_line_val(self, payslip, code):
        sql_query = """select psl.quantity,psl.rate,psl.amount from hr_payslip_line as psl where psl.slip_id = %s and psl.code = %s"""
        params = (payslip.id, code)
        self.env.cr.execute(sql_query, params)
        results = self.env.cr.dictfetchall()
        if results:
            amount = (results[0].get('amount') * results[0].get('quantity') * results[0].get('rate')) / 100
            return amount
        return 0

    def get_totals(self, lines, code_list):
        lst = []
        for c in code_list:
            lst.append(0)
        if lines:
            for line in lines:
                i = 0
                for l_val in line.get('lines'):
                    lst[i] += l_val
                    i += 1
        return lst

    def print_excel(self):
        if not self.employee_ids and self.statement_by == 'date':
            raise ValidationError(_('Please Select Employee !!!'))

        payslip_ids = self.get_payslip()
        if not payslip_ids:
            raise ValidationError(_('Payslip not Found !!!'))

        filename = 'Employee Payroll Statement.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Payroll Statement')

        # Style
        header_style = easyxf(
            'font:height 300;pattern: pattern solid, fore_color gray25; align: horiz center;font:bold True;')
        line_header = easyxf('font:height 200;align: horiz center;font:bold True;')
        group_line = easyxf(
            'font:height 200;pattern: pattern solid, fore_color gray25; align: horiz left;font:bold True;font:italic True;')
        text_right = easyxf('align: horiz right;', num_format_str='0.00')

        text_bold = easyxf('font:height 200;align: horiz center;font:bold True;')
        text_right_bold = easyxf('font:height 200;align: horiz right;font:bold True;', num_format_str='0.00')

        # column width
        worksheet.col(0).width = 55 * 55
        worksheet.col(1).width = 100 * 100
        worksheet.col(2).width = 55 * 55
        worksheet.col(3).width = 80 * 80

        worksheet.write_merge(1, 2, 1, 2, 'Employee Payroll Statement', header_style)

        if self.statement_by == 'date':
            format_start = datetime.strptime(str(self.date_from), '%Y-%m-%d')
        else:
            format_start = datetime.strptime(str(self.batch_payslip_id.date_start), '%Y-%m-%d')
        start = format_start.strftime('%d-%m-%Y')
        worksheet.write(1, 3, 'Start Date', line_header)
        worksheet.write(1, 4, start)

        if self.statement_by == 'date':
            format_end = datetime.strptime(str(self.date_to), '%Y-%m-%d')
        else:
            format_end = datetime.strptime(str(self.batch_payslip_id.date_end), '%Y-%m-%d')
        end = format_end.strftime('%d-%m-%Y')
        worksheet.write(2, 3, 'End Date', line_header)
        worksheet.write(2, 4, end)

        worksheet.write(4, 0, "Company", line_header)
        worksheet.write(4, 1, self.company_id.name, text_right)

        # Values
        code_list = self.get_code_list(payslip_ids)
        line_values = self.get_lines(payslip_ids, code_list)

        r = 6
        worksheet.write(r, 0, " ", line_header)
        worksheet.write(r, 1, "Employee Name", line_header)
        worksheet.write(r, 2, "ID", line_header)
        worksheet.write(r, 3, 'Department', line_header)
        c = 3
        for code in code_list:
            c += 1
            worksheet.write(r, c, code, line_header)
        rc = c
        if self.group_by:
            for line in line_values:
                r += 1
                worksheet.write_merge(r, r, 0, rc, line.get('month'), group_line)

                total_lst = []
                for code in code_list:
                    total_lst.append(0)

                for l_val in line.get('values'):
                    r += 1
                    worksheet.write(r, 1, l_val.get('employee'))
                    worksheet.write(r, 2, l_val.get('ID'))
                    worksheet.write(r, 3, l_val.get('department'))
                    c = 3
                    t = 0
                    for line_amount in l_val.get('lines'):
                        c += 1
                        worksheet.write(r, c, line_amount, text_right)
                        total_lst[t] = total_lst[t] + line_amount
                        t += 1

                r += 1
                worksheet.write(r, 3, 'TOTAL', text_bold)
                c = 3
                for total_l in total_lst:
                    c += 1
                    worksheet.write(r, c, total_l, text_right_bold)
                r += 1
        else:
            total_lst = []
            for code in code_list:
                total_lst.append(0)

            for l_val in line_values:
                r += 1
                worksheet.write(r, 1, l_val.get('employee'))
                worksheet.write(r, 2, l_val.get('ID'))
                worksheet.write(r, 3, l_val.get('department'))
                c = 3
                t = 0
                for line_amount in l_val.get('lines'):
                    c += 1
                    worksheet.write(r, c, line_amount, text_right)
                    total_lst[t] = total_lst[t] + line_amount
                    t += 1
            r += 1
            worksheet.write(r, 3, 'TOTAL', text_bold)
            c = 3
            for total_l in total_lst:
                c += 1
                worksheet.write(r, c, total_l, text_right_bold)
            r += 1

        fp = BytesIO()
        workbook.save(fp)
        #export_id = self.env['payroll.statement.excel'].create(
        #    {'excel_file': base64.encodebytes(fp.getvalue()), 'file_name': filename})
        #fp.close()
        var = base64.encodebytes(fp.getvalue())
        self.write({"excel_file":var,'file_name':filename})
        fp.close()
        return {
            'name': 'Employee Payroll Statement',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=payroll.statement.wizard&filename_field=file_name&field=excel_file&download=true&id=%s&filename=%s' % (self.id, filename),
            'target': 'self',
        }
        #return {
        #    'view_mode': 'form',
        #    'res_id': export_id.id,
        #    'res_model': 'payroll.statement.excel',
        #    'view_type': 'form',
        #    'type': 'ir.actions.act_window',
        #    'context': self._context,
        #    'target': 'new',
        #
        #}


class KBHRPayrollExcel(models.TransientModel):
    _name= "payroll.statement.excel"
    #excel_file = fields.Binary('Excel Report')
    #file_name = fields.Char('Excel File', size=64)

