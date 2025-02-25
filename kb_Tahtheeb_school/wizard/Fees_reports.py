from odoo import fields, models,api
from odoo import _
from datetime import datetime, date


class Fees_reports(models.TransientModel):
    _name = "fees_reports"
    _description = "Reports for Fees wizard"

    studentID_2 = fields.Many2one('student', string="Students")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    print_report = fields.Selection([('reason1', 'IN RECEIPT REPORT'), ('reason2', 'FEES COLLECTION REPORT'),
                                     ('reason3', 'Daily Cashier Report'),('reason4', 'Parent account statement report')
                                        ,('reason5', 'Student account statement report')], string='Report')
    parent_id=fields.Many2one('parent', string="Parents")
    def action_print_report(self):
        for rec in self:
            if rec.print_report == 'reason1':
                domain = []
                studentID = self.studentID_2.id
                if studentID:
                    domain += [('student_id', '=', studentID)]
                date_from = self.date_from
                if date_from:
                    domain += [('date', '>=', date_from)]
                date_to = self.date_to
                if date_to:
                    domain += [('date', '<=', date_to)]
                fees = self.env['fees'].search(domain)
                invoice_set = set()  # Use a set to store unique invoices
                invoice_list = []

                for fee in fees:
                    invoice_domain = [('partner_id.name', '=', fee.student_id.name)]
                    invoices = self.env['account.move'].search(invoice_domain)

                    for invoice in invoices:
                        payment_domain = [('partner_id', '=', invoice.partner_id.id)]
                        payment_domain += [('ref', '=', invoice.payment_reference)]
                        payments = self.env['account.payment'].search(payment_domain)

                        for payment in payments:
                            if invoice.payment_state == 'in_payment' or invoice.payment_state == 'paid':
                                vals = {
                                    'student_id': fee.student_ID,
                                    'invoice_reference': invoice.name,
                                    'account_id': invoice.invoice_line_ids[0].account_id.name,
                                    'amount': invoice.amount_total,
                                    'partner': invoice.partner_id.name,
                                    'payment': payment.journal_id.name,
                                    'date': invoice.date,
                                    'payment_amount': payment.amount,
                                    'payment_name': payment.name,
                                }
                                # Check if this invoice is already in the set
                                if invoice.name not in invoice_set:
                                    invoice_list.append(vals)
                                    invoice_set.add(invoice.name)

                data = {
                    'form_data': self.read()[0],
                    'student': invoice_list,
                    'result_ids': [],
                }
                return self.env.ref('kb_Tahtheeb_school.account_fees_312_view').report_action(self, data=data)
            elif rec.print_report == 'reason2':
                domain = []
                studentID = self.studentID_2.id
                if studentID:
                    domain += [('student_id', '=', studentID)]
                date_from = self.date_from
                # if date_from:
                #     domain += [('date', '>=', date_from)]
                date_to = self.date_to
                # if date_to:
                #     domain += [('date', '<=', date_to)]
                fees = self.env['fees'].search(domain)
                invoice_set = set()  # Use a set to store unique invoices
                invoice_list = []

                for fee in fees:
                    invoice_domain = [('partner_id.name', '=', fee.student_id.name)]
                    if date_from:
                        invoice_domain += [('invoice_date', '>=', date_from)]
                    if date_to:
                        invoice_domain += [('invoice_date', '<=', date_to)]
                    invoice = self.env['account.move'].search(invoice_domain)
                    payment_domain = [('partner_id', '=', invoice.partner_id.id)]
                    payment = self.env['account.payment'].search(payment_domain)

                    if invoice:
                        for inv in invoice:
                            # total_payment = sum(inv.payment_id.amount)
                            for pay in payment:
                                if inv.payment_state == 'in_payment' or inv.payment_state == 'paid':

                                    vals = {
                                        'student_id': fee.student_ID,
                                        'invoice_reference': inv.name,
                                        'account_id': inv.invoice_line_ids[0].account_id.name,
                                        'amount': inv.amount_total,
                                        'partner': inv.partner_id.name,
                                        'payment': inv.payment_id.journal_id.name,
                                        'date': inv.date,
                                        'payment_amount': inv.payment_id.amount,
                                        'payment_name': inv.payment_id.name,
                                        'fees_id': fee.structure_id.name,
                                        'school_fees': inv.invoice_line_ids[0].price_subtotal,
                                        'total_vat': inv.amount_tax,
                                        'amount_total': inv.amount_total,
                                        # 'payment_total': total_payment,
                                    }
                                    # Check if this invoice is already in the set
                                    if inv.name not in invoice_set:
                                        invoice_list.append(vals)
                                        invoice_set.add(inv.name)

                data = {
                    'form_data': self.read()[0],
                    'student': invoice_list,
                    'result_ids': [],
                }
                return self.env.ref('kb_Tahtheeb_school.account_fees_314_view').report_action(self, data=data)
            elif rec.print_report == 'reason4':
                domain = []
                parent_id = self.parent_id.id
                if parent_id:
                    domain += [('id', '=', parent_id)]
                parent = self.env['parent'].search(domain)
                date_from = self.date_from
                date_to = self.date_to

                parent_list = []
                for parentInfo in parent:
                    valss={
                        'parent_ids': parentInfo.ParentID,
                        'parent_id': parentInfo.name,
                    }
                    parent_list.append(valss)

                    invoice_list = []
                    vals = {}

                    for students in parent:
                        for student in students.studentID:
                            schoolt1 = 0.0
                            schoolt2 = 0.0
                            schoolt3 = 0.0

                            discountt1 = 0.0
                            discountt2 = 0.0
                            discountt3 = 0.0

                            school2t1 = 0.0
                            school2t2 = 0.0
                            school2t3 = 0.0

                            Tran1 = 0.0
                            Tran2 = 0.0
                            Tran3 = 0.0

                            Other1 = 0.0
                            Other2 = 0.0
                            Other3 = 0.0

                            nettotalt1 = 0.0
                            nettotalt2 = 0.0
                            nettotalt3 = 0.0

                            totalt1 = 0.0
                            totalt2 = 0.0
                            totalt3 = 0.0

                            tax1 = 0.0
                            tax2 = 0.0
                            tax3 = 0.0
                            fees_domine=[('student_id', '=', student.id)]
                            date_from = self.date_from
                            if date_from:
                                fees_domine += [('date', '>=', date_from)]
                            fees = self.env['fees'].search(fees_domine)
                            for fee in fees:
                                invoice_domain = [('partner_id.name', '=', fee.student_id.name)]
                                if date_from:
                                    invoice_domain += [('invoice_date', '>=', date_from)]
                                invoice = self.env['account.move'].search(invoice_domain)

                                if fee.structure_id.name == 'الرسوم الدراسية/ Tuition fees':
                                    if fee.academic_id.current:
                                        if fee.trimester == 'first-trimester':
                                            schoolt1 += fee.netTotal
                                            school2t1 += fee.Total
                                        elif fee.trimester == 'second-trimester':
                                            schoolt2 += fee.netTotal
                                            school2t2 += fee.Total
                                        elif fee.trimester == 'third-trimester':
                                            schoolt3 += fee.netTotal
                                            school2t3 += fee.Total

                                if fee.structure_id.name == 'الرسوم النقل/ Transportation fees':
                                    if fee.academic_id.current:
                                        if fee.trimester == 'first-trimester':
                                            Tran1 += fee.netTotal
                                        elif fee.trimester == 'second-trimester':
                                            Tran2 += fee.netTotal
                                        elif fee.trimester == 'third-trimester':
                                            Tran3 += fee.netTotal

                                if fee.structure_id.name == ' رسوم أخرى / Other fees':
                                    if fee.academic_id.current:
                                        if fee.trimester == 'first-trimester':
                                            Other1 += fee.netTotal
                                        elif fee.trimester == 'second-trimester':
                                            Other2 += fee.netTotal
                                        elif fee.trimester == 'third-trimester':
                                            Other3 += fee.netTotal

                                if fee.academic_id.current:
                                    if fee.trimester == 'first-trimester':
                                        nettotalt1 += fee.final_total
                                    elif fee.trimester == 'second-trimester':
                                        nettotalt2 += fee.final_total
                                    elif fee.trimester == 'third-trimester':
                                        nettotalt3 += fee.final_total

                                if fee.academic_id.current:
                                    if fee.trimester == 'first-trimester':
                                        for dis in fee.fees_line_ids:
                                            if dis.discount:
                                                discountt1 += (dis.discount/100) * dis.amount
                                    elif fee.trimester == 'second-trimester':
                                        for dis in fee.fees_line_ids:
                                            if dis.discount:
                                                discountt2 += (dis.discount/100) * dis.amount
                                    elif fee.trimester == 'third-trimester':
                                        for dis in fee.fees_line_ids:
                                            if dis.discount:
                                                discountt3 += (dis.discount/100) * dis.amount

                                if fee.academic_id.current:
                                    if fee.trimester == 'first-trimester':
                                        tax1 += fee.taxTotal
                                    elif fee.trimester == 'second-trimester':
                                        tax2 += fee.taxTotal
                                    elif fee.trimester == 'third-trimester':
                                        tax3 += fee.taxTotal

                                if invoice:
                                    for inv in invoice:
                                        if inv.id == fee.payments_line_ids.invN.id:
                                            if inv.payment_state == 'in_payment' or inv.payment_state == 'paid':
                                                if fee.trimester == 'first-trimester':
                                                    totalt1 += inv.amount_total
                                                elif fee.trimester == 'second-trimester':
                                                    totalt2 += inv.amount_total
                                                elif fee.trimester == 'third-trimester':
                                                    totalt3 += inv.amount_total

                                vals = {
                                    'student_id': fee.student_id.name,
                                    'student_ids': fee.student_id.studentID,
                                    # 'parent_ids': fee.student_id.Parent_ids.id,
                                    # 'parent_id': fee.student_id.Parent_ids.name,
                                    'school_id': fee.student_id.school_id.name,
                                    'grades': fee.student_grade.name,
                                    'schoolt1': schoolt1,
                                    'schoolt2': schoolt2,
                                    'schoolt3': schoolt3,
                                    'discountt1': discountt1,
                                    'discountt2': discountt2,
                                    'discountt3': discountt3,
                                    'school2t1': school2t1,
                                    'school2t2': school2t2,
                                    'school2t3': school2t3,
                                    'Tran1': Tran1,
                                    'Tran2': Tran2,
                                    'Tran3': Tran3,
                                    'Other1': Other1,
                                    'Other2': Other2,
                                    'Other3': Other3,
                                    'nettotalt1': nettotalt1,
                                    'nettotalt2': nettotalt2,
                                    'nettotalt3': nettotalt3,
                                    'totalt1': totalt1,
                                    'totalt2': totalt2,
                                    'totalt3': totalt3,
                                    'tax1': tax1,
                                    'tax2': tax2,
                                    'tax3': tax3,
                                }

                            invoice_list.append(vals)

                            data = {
                                'form_data': self.read()[0],
                                'student': invoice_list,
                                'parent_list': parent_list,
                            }
                return self.env.ref('kb_Tahtheeb_school.Parent_account_statement_view').report_action(self, data=data)
            elif rec.print_report == 'reason5':
                domain = []
                studentID = self.studentID_2.id
                if studentID:
                    domain += [('student_id', '=', studentID)]
                date_from = self.date_from
                if date_from:
                    domain += [('date', '>=', date_from)]
                date_to = self.date_to
                # if date_to:
                #     domain += [('date', '<=', date_to)]
                fees = self.env['fees'].search(domain)
                invoice_set = set()  # Use a set to store unique invoices
                invoice_list = []
                vals = {}
                schoolt1 =0.0
                schoolt2 =0.0
                schoolt3=0.0

                school2t1 =0.0
                school2t2 =0.0
                school2t3=0.0

                discountt1 = 0.0
                discountt2 = 0.0
                discountt3 = 0.0

                Tran1=0.0
                Tran2=0.0
                Tran3=0.0

                Other1=0.0
                Other2=0.0
                Other3=0.0

                nettotalt1=0.0
                nettotalt2=0.0
                nettotalt3=0.0

                totalt1=0.0
                totalt2=0.0
                totalt3=0.0

                tax1=0.0
                tax2=0.0
                tax3=0.0

                for fee in fees:
                    invoice_domain = [('partner_id.name', '=', fee.student_id.name)]
                    if date_from:
                        invoice_domain += [('invoice_date', '>=', date_from)]
                    if date_to:
                        invoice_domain += [('invoice_date', '<=', date_to)]
                    invoice = self.env['account.move'].search(invoice_domain)


                    if fee.structure_id.name== 'الرسوم الدراسية/ Tuition fees':
                        if fee.academic_id.current:
                            if fee.trimester=='first-trimester':
                                schoolt1 += fee.netTotal
                                school2t1 += fee.Total
                            elif fee.trimester=='second-trimester':
                                schoolt2 += fee.netTotal
                                school2t2 += fee.Total
                            elif fee.trimester=='third-trimester':
                                schoolt3 += fee.netTotal
                                school2t3 += fee.Total

                    if fee.structure_id.name== 'الرسوم النقل/ Transportation fees':
                        if fee.academic_id.current:
                            if fee.trimester=='first-trimester':
                                Tran1 += fee.netTotal
                            elif fee.trimester=='second-trimester':
                                Tran2 += fee.netTotal
                            elif fee.trimester=='third-trimester':
                                Tran3 += fee.netTotal

                    if fee.structure_id.name== ' رسوم أخرى / Other fees':
                        if fee.academic_id.current:
                            if fee.trimester=='first-trimester':
                                Other1 += fee.netTotal
                            elif fee.trimester=='second-trimester':
                                Other2 += fee.netTotal
                            elif fee.trimester=='third-trimester':
                                Other3 += fee.netTotal

                    if fee.academic_id.current:
                        if fee.trimester == 'first-trimester':
                            for dis in fee.fees_line_ids:
                                if dis.discount:
                                    discountt1 += (dis.discount / 100) * dis.amount
                        elif fee.trimester == 'second-trimester':
                            for dis in fee.fees_line_ids:
                                if dis.discount:
                                    discountt2 += (dis.discount / 100) * dis.amount
                        elif fee.trimester == 'third-trimester':
                            for dis in fee.fees_line_ids:
                                if dis.discount:
                                    discountt3 += (dis.discount / 100) * dis.amount

                    if fee.academic_id.current:
                        if fee.trimester == 'first-trimester':
                            nettotalt1 += fee.final_total
                        elif fee.trimester =='second-trimester':
                            nettotalt2 += fee.final_total
                        elif fee.trimester == 'third-trimester':
                            nettotalt3 += fee.final_total

                    if fee.academic_id.current:
                        if fee.trimester=='first-trimester':
                            tax1 += fee.taxTotal
                        elif fee.trimester=='second-trimester':
                            tax2 += fee.taxTotal
                        elif fee.trimester=='third-trimester':
                            tax3 += fee.taxTotal

                    if invoice:
                        for inv in invoice:
                            if inv.id == fee.payments_line_ids.invN.id:
                                if inv.payment_state == 'in_payment' or inv.payment_state == 'paid':
                                    if fee.trimester == 'first-trimester':
                                        totalt1 += inv.amount_total
                                    elif fee.trimester == 'second-trimester':
                                        totalt2 += inv.amount_total
                                    elif fee.trimester == 'third-trimester':
                                        totalt3 += inv.amount_total
                    vals = {
                        'student_id': fee.student_id.name,
                        'student_ids': fee.student_id.studentID,
                        'parent_ids': fee.student_id.Parent_ids.id,
                        'parent_id': fee.student_id.Parent_ids.name,
                        'school_id': fee.student_id.school_id.name,
                        'grades': fee.student_grade.name,
                        'schoolt1':schoolt1,
                        'schoolt2': schoolt2,
                        'schoolt3': schoolt3,
                        'school2t1':school2t1,
                        'school2t2': school2t2,
                        'school2t3': school2t3,
                        'Tran1': Tran1,
                        'Tran2': Tran2,
                        'Tran3': Tran3,
                        'Other1': Other1,
                        'Other2': Other2,
                        'Other3': Other3,
                        'discountt1': discountt1,
                        'discountt2': discountt2,
                        'discountt3': discountt3,
                        'nettotalt1': nettotalt1,
                        'nettotalt2': nettotalt2,
                        'nettotalt3': nettotalt3,
                        'totalt1': totalt1,
                        'totalt2': totalt2,
                        'totalt3': totalt3,
                        'tax1': tax1,
                        'tax2': tax2,
                        'tax3':tax3,
                    }

                invoice_list.append(vals)

                data = {
                    'form_data': self.read()[0],
                    'student': invoice_list,
                }
                return self.env.ref('kb_Tahtheeb_school.Student_account_statement_view').report_action(self, data=data)








