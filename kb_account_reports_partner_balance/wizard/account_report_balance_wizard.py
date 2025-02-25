from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountReportWizard(models.TransientModel):
    _name = 'account.report.balance.wizard'

    result_selection = fields.Selection([('customer', 'Receivable Accounts'),
                                         ('supplier', 'Payable Accounts')
                                         ], string="Partner's", required=True, default='customer')
    
    partner_date = fields.Date(string="Date", default=datetime.today())

    def result_selection2(self):
        m = ""
        if self.result_selection == 'customer':
            m = "'Receivable'"
        elif self.result_selection == 'supplier':
            m = "'Payable'"

        return m

    def _sql_from_center_lines(self):
        bb = self.result_selection2()
        partner_dates = self.partner_date
        # "account_move_line".full_reconcile_id IS NULL  and
        sql = """SELECT  "account_move_line".partner_id, (select name from res_partner where id = account_move_line.partner_id) as partner_id, sum("account_move_line".debit) as debit, sum("account_move_line".credit) as credit, sum("account_move_line".debit - "account_move_line".credit)  as balance
            FROM account_move_line
            LEFT JOIN account_account acc ON ("account_move_line".account_id = acc.id)
            LEFT JOIN account_move m ON (m.id="account_move_line".move_id)
            WHERE  acc.account_type = """ + bb + """
            and "account_move_line".date <= '""" + str(partner_dates) + """'
            group by "account_move_line".partner_id
            HAVING sum("account_move_line".debit - "account_move_line".credit) <> 0"""
        return sql

    def print_pdf(self):
        output = []
        # data = []
        sql = self._sql_from_center_lines()
        # tables, where_clause, where_params = self.env['account.move.line']._query_get()
        query = sql  # % (tables, where_clause)

        self.env.cr.execute(query)
        results = self.env.cr.fetchall()

        for result in results:
            # raise ValidationError(_("{} after the for\n").format(result))
            # output[result[0]] = result[4]
            output.append({
                'id': result[0],
                'name': result[1],
                'credit': result[2],
                'debit': result[3],
                'balance': result[4],
                # 'date': result[5],
            })

        data = {
            'form_data': self.read()[0],
            'out_list': output,
        }
            # raise ValidationError(_("{} after the for\n").format(len(result)))
        return self.env.ref('kb_account_reports_partner_balance.action_account_report_balance_template').report_action(self, data=data)

    # def print_pdf(self):
    #     # date_from = self.date_from
    #     # date_to = self.date_to
    #     # self.check_date_range()
    #     query = """SELECT  "account_move_line".partner_id, (select name from res_partner where id = account_move_line.partner_id) as partner_id, sum("account_move_line".debit) as debit, sum("account_move_line".credit) as credit, sum("account_move_line".debit - "account_move_line".credit)  as balance
    #         FROM account_move_line
    #         LEFT JOIN account_account acc ON ("account_move_line".account_id = acc.id)
    #         LEFT JOIN account_move m ON (m.id="account_move_line".move_id)
    #         WHERE   "account_move_line".full_reconcile_id IS NULL  and acc.name = 'Account Receivable'
    #         group by "account_move_line".partner_id
    #         HAVING sum("account_move_line".debit - "account_move_line".credit) > 0"""
    #
    #     self.env.cr.execute(query)
    #     invoice = self.env.cr.fetchall()
    #     i = 0
    #     datas = []
    #     for line in invoice:
    #         datas.append({
    #             'datas_id': line,
    #         })
    #     print("Account", datas)
    #     return self.env.ref('kb_account_reports_partner_balance.action_account_report_template').report_action(self, data=datas)


