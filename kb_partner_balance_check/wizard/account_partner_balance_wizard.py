from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import xlwt
from io import BytesIO
import base64
from xlwt import easyxf

class AccountReportWizardBalanceCheck(models.TransientModel):
    _name = 'account.partner.balance.check.wizard'

    date_to = fields.Date(string="Date To",default=fields.Date.context_today, required="1")
    account_ids = fields.Many2one('account.account', string="Account ID", required="1")
    partner_ids = fields.Many2one('res.partner', string="Partner ID", required="1")

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)
    
    def _sql_from_center_lines(self):

        sql = """select (sum(debit) - sum(credit)) as balanceBegin,'0' as debit, '0' as credit, '0' as balanceEnd  , (select p.name from res_partner p where p.id= m.partner_id   ) as partner_name
from account_move_line m 
where    account_id = {} and m.partner_id = {} and   date < '{}'
group by partner_id 
 """.format(self.account_ids.id,self.partner_ids.id,self.date_to)
        return sql

    def print_pdf(self):
        output = []
        data = []
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
        return self.env.ref('kb_partner_balance_check.action_account_partner_report_template').report_action(self, data=data)

        # print Excel
    # account_report_balance_check



