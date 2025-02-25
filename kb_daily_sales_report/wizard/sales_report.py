from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class SalesReportWiz(models.TransientModel):
    _name = "sales.report.wiz"
    _description = "Sales Report Wizard"

    # branch_ids = fields.Many2one('res.branch', string='Branch')
    date_from = fields.Date(string='From Date', required=True, default=fields.Date.today())
    date_to = fields.Date(string='To Date', required=True, default=fields.Date.today())
    type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor')], string='Type', default='customer', required=True)

    company_logo = fields.Binary()

    def generate_report(self):
        output = []
        payment_vals = []
        payment_journal_vals = {}
        # Getting Invoices
        self.company_logo = self.env.company.logo

        type = 'partner_id.customer_rank'
        if self.type == 'supplier':
            type = 'partner_id.supplier_rank'

        payment_journals = []
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                  (type, '>', 0), ('state', '=', 'posted')]
        
        # branch_ids = self.branch_ids
        # if branch_ids:
        #     domain += [('branch_id','=',branch_ids.id)]
        if self.type == 'customer':
            domain.append(('move_type', 'in', ['out_invoice', 'out_refund']))
        else:
            domain.append(('move_type', 'in', ['in_invoice', 'in_refund']))


        account_move_ids = self.env['account.move'].search(domain)
        
        for move in account_move_ids:
            so_number = ''
            for inv_line in move.invoice_line_ids:
                so_number += ','.join(inv_line.mapped('sale_line_ids').mapped('order_id.name'))
            output.append({
                'date': move.date,
                'name': move.partner_id.name,
                'reference': move.name,
                'move_type': move.move_type,
                'payment_id': move.payment_id and move.payment_id or False,
                'type': self.type,
                'due_date': move.invoice_date_due,
                'journal_code': move.journal_id.code,
                'sale_order': so_number,
                'salesman': move.invoice_user_id.name,
                'total': move.amount_total_signed,
                'total_due': move.amount_residual,
            })
            if move.payment_id:
                payment_journals.append(move.journal_id.code)
            payment_ids = self.env['account.payment'].search([])

            if self.type == 'customer':
                for payment in payment_ids:
                    if payment.date >= self.date_from and payment.date <= self.date_to :
                        if move.id in payment.reconciled_invoice_ids.ids:
                            payment_vals.append({
                                'date': payment.date,
                                'name': payment.name,
                                'partner_id': payment.partner_id.name,
                                'journal_code': payment.journal_id.name,
                                'move_id': move.name,
                                'user_id': payment.user_id.name,
                                'amount': payment.amount_total_signed
                            })
            else:
                for payment in payment_ids:
                    if payment.date >= self.date_from and payment.date <= self.date_to :
                        if move.id in payment.reconciled_bill_ids.ids:
                            payment_vals.append({
                                'date': payment.date,
                                'name': payment.name,
                                'partner_id': payment.partner_id.name,
                                'journal_code': payment.journal_id.name,
                                'move_id': move.name,
                                'user_id': payment.user_id.name,
                                'amount': move.amount_total_signed
                            })
        payment_total = {key: 0.0 for key in payment_journals}

        total = 0.0
        for line in payment_vals:
            if line.get('journal_code') not in payment_journal_vals:
                payment_journal_vals.update({
                    line.get('journal_code'): total
                })
            else:
                payment_journal_vals[line.get('journal_code')] = total
        for line in payment_vals:
            if line.get('journal_code') in payment_journal_vals.keys():
                payment_journal_vals[line.get('journal_code')] = payment_journal_vals[line.get('journal_code')] + line.get('amount')

        return self.env.ref(
            'kb_daily_sales_report'
            '.action_report_daily_invoice').with_context(landscape=False).report_action(
            self, data={'moves': output,
                        'payment_total': payment_total,
                        'payment_journals': payment_journal_vals,
                        'payment_vals': payment_vals,
                        'wizard': self.read()[0],
                        'type': self.type,
                        'company_logo':self.env.company.logo,

                        'company_name': self.env.company.name,
                        'company_street':self.env.company.street,
                        'company_city':self.env.company.city,
                        'company_zip':self.env.company.zip,
                        'company_country':self.env.company.country_id.name,
                        'company_phone': self.env.company.phone,
                        'company_email': self.env.company.email,
                        'company_websites':self.env.company.website,
                        'company_vat': self.env.company.vat
                        })

    # Report Excel Method 
    def generate_report_ex(self):  

        # Getting Invoice
        type = 'partner_id.customer_rank'
        if self.type == 'supplier':
            type = 'partner_id.supplier_rank'

        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                  (type, '>', 0), ('state', '=', 'posted')]
        
        # branch_ids = self.branch_ids
        # if branch_ids:
        #     domain += [('branch_id','=',branch_ids.id)]

        if self.type == 'customer':
            domain.append(('move_type', 'in', ['out_invoice', 'out_refund']))
        else:
            domain.append(('move_type', 'in', ['in_invoice', 'in_refund']))

    
        account_move_ids = self.env['account.move'].search_read(domain)
        
        
        # Getting payment 
        account_move = self.env['account.move'].search([])
        payment_move_ids = self.env['account.payment'].search([]) 

        

        domains = [('date', '>=', self.date_from),('date', '<=', self.date_to),(type, '>', 0)]

        # branch_idss = self.branch_ids
        # if branch_idss:
        #     domains += [('branch_id','=',branch_ids.id)]
    
        if self.type == 'customer':
            for payment in payment_move_ids:
                for move in account_move:
                        if move.id in payment.reconciled_invoice_ids.ids:
                            payment_move_ids = self.env['account.payment'].search_read(domains)
        else:
            for payment in payment_move_ids:
                for move in account_move:
                        if move.id in payment.reconciled_invoice_ids.ids:
                            payment_move_ids = self.env['account.payment'].search_read(domains)
                

        data = {
            'payment_ids' : payment_move_ids,
            'move_ids': account_move_ids, 
            'form_data': self.read()[0],
            }

        return self.env.ref('kb_daily_sales_report.action_print_report_xlsx').report_action(self, data=data)