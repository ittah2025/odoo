from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf

class AccountReportWizardBydate(models.TransientModel):
    _name = 'account.partner.report.wizard'

    date_from = fields.Date(string="Date From",default=fields.Date.context_today, required="1")
    date_to = fields.Date(string="Date To",default=fields.Date.context_today, required="1")
    account_ids = fields.Many2one('account.account', string="Account ID", required="1")

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)
    
    def _sql_from_center_lines(self):

        sql = """select sum(balancebegin) as balancebegin, sum(debit) as debit, sum(credit) as credit, sum(balancebegin+debit-credit) as balanceend, partner_name
        from (select (sum(debit) - sum(credit)) as balanceBegin,'0' as debit, '0' as credit, '0' as balanceEnd  , (select p.name from res_partner p where p.id= m.partner_id   ) as partner_name
        from account_move_line m 
        where    account_id = {} and m.partner_id is not null and   date < '{}'
        group by partner_id 
        union all 
        select '0' as balanceBegin,sum(debit) as sumDebit,sum(credit) as sumCredit, sum(debit) - sum(credit), (select p.name from res_partner p where p.id= mm.partner_id   ) as partner_name
        from account_move_line mm 
        where    mm.account_id = {}  and mm.partner_id is not null and date between '{}' and '{}'
        group by partner_id ) h
        group by partner_name""".format(self.account_ids.id,self.date_from,self.account_ids.id,self.date_from,self.date_to)
        return sql

    def print_pdf(self):
        output = []
        sql = self._sql_from_center_lines()
        # tables, where_clause, where_params = self.env['account.move.line']._query_get()
        query = sql  # % (tables, where_clause)

        self.env.cr.execute(query)
        results = self.env.cr.fetchall()

        for result in results:
            # raise ValidationError(_("{} after the for\n").format(result))
            # output[result[0]] = result[4]
            output.append({
                'balancebegin': result[0],
                'debit': result[1],
                'credit': result[2],
                'balanceend': result[3],
                'partner_name': result[4],
            })

        data = {
            'form_data': self.read()[0],
            'out_list': output,
        }
            # raise ValidationError(_("{} after the for\n").format(len(result)))
        return self.env.ref('kb_partner_account.action_account_partner_report_template').report_action(self, data=data)

        # print Excel
    def print_excel(self):
        print("EXCEL TEST")
        output = []
        # data = {
        #     'form_data': self.read()[0],
        #     'email': "TEST@example.com",
        # }
        filename = 'Account Report by date.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        sql = self._sql_from_center_lines()
        query = sql 

        self.env.cr.execute(query)
        results = self.env.cr.fetchall()
        for result in results:
            # raise ValidationError(_("{} after the for\n").format(result))
            # output[result[0]] = result[4]
            output.append({
                'balancebegin': result[0],
                'debit': result[1],
                'credit': result[2],
                'balanceend': result[3],
                'partner_name': result[4],
            })

        bold = xlwt.easyxf( 'font: bold on; align: wrap on, vert centre, horiz center;\
                               borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                                pattern: pattern solid, fore_color white;\
                                align: horiz center,' )


        style = xlwt.easyxf('font: bold off, color black;\
                    borders: top_color black, bottom_color black, right_color black, left_color black,\
                            left thin, right thin, top thin, bottom thin;\
                    pattern: pattern solid, fore_color white;\
                                align: horiz center,')
        
        
        

        title_style = xlwt.easyxf('font: bold on, color black;\
                    borders: top_color black, bottom_color black, right_color black, left_color black,\
                            left thin, right thin, top thin, bottom thin;\
                    pattern: pattern solid, fore_color white;\
                                align: horiz center;\
                                    font: height 340,')
        
        style2_date = xlwt.easyxf('align: wrap on, vert centre, horiz center', num_format_str='DD-MMM-YYYY')

        worksheet.col(0).width = 5000
        worksheet.row(6).height = 1000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 8000
        worksheet.col(3).width = 8000
        worksheet.col(4).width = 8000
        worksheet.col(5).width = 8000
        seq = 1
        total_debit = 0
        total_credit = 0
        total_balanceend = 0
        total_balancebegin = 0
        worksheet.write_merge(1, 2, 3, 4, 'تقرير رصيد الشريك', title_style)
        worksheet.write(4, 0, 'Date From',bold)
        worksheet.write(4, 1, self.date_from,style2_date)
        worksheet.write(4, 3, 'Date To',bold)
        worksheet.write(4, 4, self.date_to,style2_date)
        worksheet.write(6, 0, 'NO \n م',bold)
        worksheet.write(6, 1, 'PARTNER NAME \n اسم العميل',bold)
        worksheet.write(6, 2, 'BALANCE BEGIN \n الرصيد الافتتاحي',bold)
        worksheet.write(6, 3, 'DEBIT \n مدين',bold)
        worksheet.write(6, 4, 'CREDIT \n دائن',bold)
        worksheet.write(6, 5, 'BALANCE END \n الرصيد النهائي',bold)
        rows = 7
        for line in output:
            if line['balanceend'] != 0:
                worksheet.write(rows, 0, seq,style)
                worksheet.write(rows, 1, line['partner_name'],style)
                worksheet.write(rows, 2, line['balancebegin'],style)
                worksheet.write(rows, 3, line['debit'],style)
                worksheet.write(rows, 4, line['credit'],style)
                worksheet.write(rows, 5, line['balanceend'],style)

                rows += 1
                seq += 1
                total_balancebegin = total_balancebegin + line['balancebegin']
                total_debit = total_debit + line['debit']
                total_credit = total_credit + line['credit']
                total_balanceend = total_balanceend + line['balanceend']

        worksheet.write(rows, 0, '',bold)
        worksheet.write(rows, 1, 'TOTAL',bold)
        worksheet.write(rows, 2, total_balancebegin,bold)
        worksheet.write(rows, 3, total_debit,bold)
        worksheet.write(rows, 4, total_credit,bold)
        worksheet.write(rows, 5, total_balanceend,bold)
        worksheet.row(rows).height = 450
        fp = BytesIO()
        workbook.save(fp)
        var = base64.encodestring(fp.getvalue())
        self.write({"excel_file":var,'file_name':filename})
        fp.close()
        return {
            'name': 'Account Report',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=account.partner.report.wizard&filename_field=file_name&field=excel_file&download=true&id=%s&filename=%s' % (self.id, filename),
            'target': 'self',
        }



