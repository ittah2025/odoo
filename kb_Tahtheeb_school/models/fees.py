from email.policy import default
# from typing_extensions import Required
from odoo import api, fields, models , _
from datetime import date
from odoo.exceptions import UserError, ValidationError
import re
from odoo.tools.translate import _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class fees(models.Model):
    _name = "fees"
    _table = "fees"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "fees"
    _rec_name = "student_id"

    date = fields.Date(string="Date", help="Enter the date of fees",required=True)

    student_id = fields.Many2one('student', string="Student ID",
                                 help='Select school')

    student_ID = fields.Char(string="Student ID", related="student_id.studentID")
    student_grade = fields.Many2one('grade', string="Gtrade", related="student_id.grades")
    student_nationality = fields.Selection([
        ('', ''),
    ], related="student_id.nationality")

    parent_id = fields.Many2one('parent')
    siblings = fields.Integer(string="Siblings", related="student_id.siblings")

    trimester = fields.Selection([('first-trimester', 'First Trimester'),
                                  ('second-trimester','Second Trimester'),
                                  ('third-trimester', 'third Trimester')], string="Trimester",default='first-trimester', required=True)
    academic_id=fields.Many2one('academic_year',string='Academic year')

    @api.onchange("student_id")
    def siblings_number(self):
        self.siblings = self.student_id.Parent_ids.childs - 1

    school_id = fields.Many2one('school', string="School",
                                help='Select school')

    academic_year_id = fields.Many2one('academic_year', string="academic year",
                                       help='Select academic year')

    grades_id = fields.Many2many('grade', string="grade", help='Select grade')

    class_id = fields.Many2many('classes', string="classes",
                                help='Select class')

    structure_id = fields.Many2one('fees_structure', string="Fees Structure",
                                   help='Select The structure of the fees')

    journal_id = fields.Many2one('account.journal', string="journal")

    Total= fields.Float(string="Untaxed Amount:",compute="calculat_total_untax")
    netTotal= fields.Float(string="Total:",compute="calculat_Net_Total")
    taxTotal= fields.Float(string="Tax:",compute="calculat_total_tax")


    # calculate final total without tax
    def calculat_total_untax(self):
        total = 0
        for t in self.fees_line_ids:
            total += t.subtotal
        self.Total = total

    # calculate final total
    def calculat_total_tax(self):
        total = 0
        taxs = 0
        for t in self.fees_line_ids:
            total += t.subtotal
            taxs = t.tax
        self.taxTotal = total * (int(taxs)/100 )

    # calculate final total
    @api.onchange("netTotal")
    def calculat_Net_Total(self):
        for rec in self:
            rec.netTotal = rec.taxTotal + rec.Total


    @api.onchange("structure_id")
    def onchange_fees_structure_id(self):
        # raise  ValidationError(_('Changed'))
        """"Method to  change respective fees structure details on changing of fees_structure_id"""
        parent = self.env['parent'].search([('id', '=', self.student_id.Parent_ids.id)])
        structure = self.env['fees_structure'].search([('id', '=', self.structure_id.id)])
        if self.structure_id.id == 1:
            yearly_fees = self.env['student.yearly.fees'].search([('grade', '=', self.student_id.grades.id)])
            # raise ValidationError(_(yearly_fees))
            for rec in self:
                # if not self.fees_line_ids: #if the many2many field not empty then write direct
                rec.fees_line_ids = [(5, 0, 0)]
                lines = [(5, 0, 0)]
                for data in yearly_fees:
                    if rec.has_dicount == False:
                        if (self.student_nationality == 'Saudi' or self.student_nationality == 'NonSaudi') and (
                                parent.othernationality == 'saudi' or parent.nationality == 'Saudi'):
                            line_vals = {

                                "name": rec.structure_id.name,
                                "code": rec.structure_id.code,
                                'quantity':1,
                                "account": rec.journal_id.name,
                                "tax": '0',
                                "amount": data.t1,
                            }
                            lines.append((0, 0, line_vals))
                        elif self.student_nationality == 'NonFSaudi':
                            line_vals = {

                                "name": rec.structure_id.name,
                                "code": rec.structure_id.code,
                                "account": rec.journal_id.name,
                                'quantity': 1,
                                "tax": '15',
                                "amount": data.t1,

                            }
                            lines.append((0, 0, line_vals))
                    elif rec.has_dicount == True:
                        if (self.student_nationality == 'Saudi' or self.student_nationality == 'NonSaudi') and (
                                parent.othernationality == 'saudi' or parent.nationality == 'Saudi'):
                            line_vals = {

                               "name": rec.structure_id.name,
                                "code": rec.structure_id.code,
                                'discount': 5,
                                "account": rec.journal_id.name,
                                'quantity': 1,
                                "tax": '0',
                                 "amount": data.t1,

                            }
                            lines.append((0, 0, line_vals))

                        elif self.student_nationality == 'NonSaudi':
                            line_vals = {

                                "name": rec.structure_id.name,
                                "code": rec.structure_id.code,
                                'discount': float(data.amount) * 0.05,
                                "account": rec.journal_id.name,
                                'quantity': 1,
                                "tax": '15',
                                "amount": data.t1,

                            }
                            lines.append((0, 0, line_vals))
                    rec.write({"fees_line_ids": lines})

        else:
            for rec in self:
                # if not self.fees_line_ids: #if the many2many field not empty then write direct
                rec.fees_line_ids = [(5, 0, 0)]
                lines = [(5, 0, 0)]
                for record in structure:
                    for data in record.fees_structure_line_ids:
                        if rec.has_dicount == False:
                            if (self.student_nationality == 'Saudi' or self.student_nationality == 'NonSaudi') and (
                                    parent.othernationality == 'saudi' or parent.nationality == 'Saudi'):
                                line_vals = {

                                    "name": data.name,
                                    "code": data.code,
                                    'quantity':1,
                                    "account": rec.journal_id.name,
                                    "tax": '0',
                                    "amount": data.amount,
                                }
                                lines.append((0, 0, line_vals))
                                # raise ValidationError(_(lines))
                            elif self.student_nationality == 'NonFSaudi':
                                line_vals = {

                                    "name": data.name,
                                    "code": data.code,
                                    'quantity':1,
                                    "account": rec.journal_id.name,
                                    "tax": '15',
                                    "amount": data.amount,

                                }
                                lines.append((0, 0, line_vals))
                        elif rec.has_dicount == True:
                            if (self.student_nationality == 'Saudi' or self.student_nationality == 'NonSaudi') and (
                                    parent.othernationality == 'saudi' or parent.nationality == 'Saudi'):
                                line_vals = {

                                    "name": data.name,
                                    "code": data.code,
                                    'quantity':1,
                                    'discount':5,
                                    "account": rec.journal_id.name,
                                    "tax": '0',
                                    "amount": data.amount,

                                }
                                lines.append((0, 0, line_vals))

                            elif self.student_nationality == 'NonSaudi':
                                line_vals = {

                                    "name": data.name,
                                    "code": data.code,
                                    'quantity':1,
                                    'discount': float(data.amount) * 0.05,
                                    "account": rec.journal_id.name,
                                    "tax": '15',
                                    "amount": data.amount,


                                }
                                lines.append((0, 0, line_vals))
                        rec.write({"fees_line_ids": lines})


    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('done', 'Done'),
    ], readonly=True, default="draft", help='Choose the fees state')

    payment_type = fields.Selection([
        ('full', 'Full'),
        ('half', 'Half'),
        ('month', 'Month'),
    ], string="Payment Type", required=True, help='Choose the payment type')

    paymentNumber = fields.Integer(string="Payment Number")

    nationality = fields.Selection([
        ('saudi', 'Saudi'),
        ('non', 'Non'),
    ], string="Nationality", required=False, help='Choose the student nationality')

    fees_structure = fields.Selection([
        ('regeisterion', 'Regeisterion Fees'),
        ('school', 'School Fees'),
    ], string="Fees Strucutre", required=False, help='Choose the Fees Strucutre')

    fees_line_ids = fields.One2many('fees_line', 'fees_line_id', string="fees line")

    payments_line_ids = fields.One2many('payments_line', 'payments_line_id', string="payments line")

    total_amount = fields.Float(string="Total Amount", store=True, readonly=True, compute='compute_amount',
                                help="Total amount")

    balance_amount = fields.Float(string="Balance Amount", store=True, compute='compute_amount', help="Balance amount")

    total_paid_amount = fields.Float(string="Total Paid Amount", store=True, compute='compute_amount',
                                     help="Total paid amount")

    def count_pyment(self):
        for rec in self:
            if rec.payment_type=="full":
                rec.paymentNumber=1
            elif rec.payment_type=="half":
                rec.paymentNumber=2

            return rec.paymentNumber

    def compute_amount(self):
        total_paid = 0.0
        for rec in self:
            for line in rec.payments_line_ids:
                if line.isPaid:
                    total_paid += line.total
            balance_amount = rec.netTotal - total_paid
            rec.total_amount = rec.netTotal
            rec.balance_amount = balance_amount
            rec.total_paid_amount = total_paid

    def payments(self):
        for rec in self:
            if rec.payment_type!="month":
                rec.paymentNumber = rec.count_pyment()
            rec.payments_line_ids.unlink()
            startDate = datetime.strptime(str(rec.date), '%Y-%m-%d')
            total = rec.netTotal / (int(rec.paymentNumber))
            for i in range(1, (int(rec.paymentNumber)) + 1):
                self.env['payments_line'].create({
                    'sr': i + 0,
                    'payments_line_id': self.id,
                    'payment_date': startDate,
                    'total': total,

                })
                startDate = startDate + relativedelta(months=1)
            rec.compute_amount()
        return True

    invoice_ids_num=fields.Char(string="Fees Count", compute="compute_invoice")

    def compute_invoice(self):
        for rec in self:
            invoice_ids = self.env['account.move'].search_count([('partner_id.name', '=', self.student_id.name)])
            rec.invoice_ids_num = invoice_ids

    def action_open_invoice(self):
        domain = [('partner_id.name', '=', self.student_id.name)]
        return {
            'name': _('Invoice'),
            'domain': domain,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'current'
        }

    invoices_count = fields.Integer(compute='_invoices_count', string='# Invoices')


    siblings_line_ids = fields.One2many('siblings_line', 'siblings_line_id', string="siblings line")

    @api.onchange("student_id")
    def get_Siblings(self):
        for rec in self:
            rec.siblings_line_ids = [(5, 0, 0)]
            lines = [(5, 0, 0)]
            count=0
            for data in rec.student_id.Parent_ids.studentID:
                if data.id != rec.student_id.id:
                    line_vals = {
                        "sr":count,
                        "student_id": data.id,
                        "studentID": data.studentID,
                        'admissionDate': data.admissionDate,
                    }
                    lines.append((0, 0, line_vals))
                    count+=1

            rec.write({"siblings_line_ids": lines})

    has_dicount = fields.Boolean(string="Has Discount", default=False)

    @api.onchange('date')
    def check_siblings_discount(self):
        for rec in self:
            for record in rec.siblings_line_ids:
                if rec.siblings == 0 :
                    pass
                elif rec.siblings <= 2 and rec.siblings > 0:
                    if rec.student_id.admissionDate < record.admissionDate :
                        rec.has_dicount = False
                    elif rec.student_id.admissionDate > record.admissionDate :
                        rec.has_dicount = True

    final_total = fields.Float(string="الأجمالي المستحق", readonly=True, compute="_calculat_total_final")

    @api.depends('final_total')
    def _calculat_total_final(self):
        totals = 0
        for t in self.payments_line_ids:
            if t.isPaid == False:
                totals += t.total
        self.final_total = totals

    subFinal_total = fields.Float(string="الاجمالي المدفوع", readonly=True, compute="_calculat_sub_total_final")

    @api.depends('subFinal_total')
    def _calculat_sub_total_final(self):
        subTotals = 0
        for t in self.payments_line_ids:
            if t.isPaid == True:
                subTotals += t.total
        self.subFinal_total = subTotals

class fees_line(models.Model):
    _name = 'fees_line'
    _description = 'fees line'

    name = fields.Char(string="Name", help="Name")

    code = fields.Char(string="Code", help='')

    account = fields.Char(string="Account", help="")

    discount = fields.Integer(string="Discount (%)")

    amount = fields.Integer(string="Amount")
    quantity=fields.Integer(string="Quantity")
    subtotal = fields.Integer(string="Subtotal", compute="n")

    tax = fields.Selection([
        ('0', '0%'),
        ('15', '15%'),
    ], string="Tax", required=False, help='Choose the Tax')

    fees_line_id = fields.Many2one('fees', string='fees line')

    @api.onchange("amount", "discount", "tax")
    def n(self):
        for rec in self:
            if (rec.discount != 0):
                new_subtotal = rec.amount - ((rec.discount) / 100 * rec.amount)
                if (rec.tax == "15"):
                    new_subtotal = new_subtotal + (0.15 * rec.amount)
                    rec.subtotal = new_subtotal
                else:
                    rec.subtotal = new_subtotal

            else:
                if (rec.tax == "15"):
                    new_subtotal = rec.amount + (0.15 * rec.amount)
                    rec.subtotal = new_subtotal
                else:
                    rec.subtotal = rec.amount


class Analictic_account(models.Model):
    _inherit = "product.template"

    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )
    analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line', inverse_name='move_line_id',
        string='Analytic lines',
    )
    move_id = fields.Many2one('account.move',
        string='Journal Entry',
        required=False,
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,
    )
    parent_state = fields.Selection(related='move_id.state', store=True)
    analytic_distribution = fields.Json( 'Analytic',
        inverse="_inverse_analytic_distribution",
    )  # add the inverse function used to trigger the creation/update of the analytic lines accordingly (field originally defined in the analytic mixin)


    @api.onchange('analytic_distribution')
    def _inverse_analytic_distribution(self):
        """ Unlink and recreate analytic_lines when modifying the distribution."""
        lines_to_modify = self.env['account.move.line'].browse([
            line.id for line in self if line.parent_state == "posted"
        ])
        lines_to_modify.analytic_line_ids.unlink()
        lines_to_modify._create_analytic_lines()

    def _create_analytic_lines(self):
        """ Create analytic items upon validation of an account.move.line having an analytic distribution.
        """
        self._validate_analytic_distribution()
        analytic_line_vals = []
        for line in self:
            analytic_line_vals.extend(line._prepare_analytic_lines())

        self.env['account.analytic.line'].create(analytic_line_vals)

    def _validate_analytic_distribution(self):
        for line in self.filtered(lambda line: line.display_type == 'product'):
            line._validate_distribution(**{
                'product': line.product_id.id,
                'account': line.account_id.id,
                'business_domain': line.move_id.move_type in ['out_invoice', 'out_refund', 'out_receipt'] and 'invoice'
                                   or line.move_id.move_type in ['in_invoice', 'in_refund', 'in_receipt'] and 'bill'
                                   or 'general',
                'company_id': line.company_id.id,
            })

class siblings_lines(models.Model):
    _name = 'siblings_line'
    _description = 'siblings line'

    siblings_line_id = fields.Many2one('fees', string="Student ID", required=False)

    student_id= fields.Many2one('student', string="Student ID", required=False)

    sr=fields.Integer(string='Sr', required=False)

    studentID = fields.Char(string='Student ID', required=False)

    admissionDate = fields.Date(string='Admission Date', required=False)

class payments_line(models.Model):
    _name = 'payments_line'
    _description = 'payments line'

    payments_line_id = fields.Many2one('fees', string="payments", required=False)

    sr=fields.Integer(string='Sr', required=False)

    payment_date=fields.Date(string='Payment Date', required=False)

    total = fields.Float(string="Total")

    isPaid = fields.Boolean(string='Paid?', readonly=False, default=False)
    invName = fields.Many2one('sale.order')
    invN = fields.Many2one('sale.order')

    def create_invoices(self):
        for rec in self:
            today_date = date.today()
            account_inv_obj = self.env['account.move']
            fees=self.env['fees'].search([('id','=',self.payments_line_id.id)])
            fees_id = self.env['fees_line'].search([('fees_line_id', '=', fees.id)])
            name_student = self.env['res.partner'].search([('email', '=', fees.student_id.email)])
            product_obj = self.env['product.template'].search([('name', '=', fees.structure_id.name)])
            tax = self.env['account.tax'].search([('id', '=', 1)])
            tax_2 = self.env['account.tax'].search([('id', '=', 2)])
            sale_id = self.env['sale.order'].create({
                'partner_id': name_student.id,
                'date_order': today_date,
            })
            sale_order_line = []
            for reco in fees:
                for record in fees_id:
                    if record.tax == '15':
                        sale_order_line.append(self.env['sale.order.line'].create({
                            'name': record.name,
                            'product_id': reco.structure_id.id,
                            'discount': record.discount,
                            'tax_id': tax,
                            'product_uom_qty': record.quantity,
                            'analytic_distribution': product_obj.analytic_distribution,
                            'price_unit': record.amount/reco.paymentNumber,
                            'order_id': sale_id.id,
                        })
                        )
                    elif record.tax == '0':
                        sale_order_line.append(self.env['sale.order.line'].create({
                            'name': record.name,
                            'product_id': reco.structure_id.id,
                            'discount': record.discount,
                            'tax_id': tax_2,
                            'product_uom_qty': record.quantity,
                            'analytic_distribution': product_obj.analytic_distribution,
                            'price_unit': record.amount/reco.paymentNumber,
                            'order_id': sale_id.id,
                        })
                        )

            sale_id.action_confirm()
            Sale_idss=sale_id._create_invoices()
            # raise ValidationError(_(Sale_idss))
            rec.invN=Sale_idss.id
            if sale_id:
                self.isPaid = True

