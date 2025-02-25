# See LICENSE file for full copyright and licensing details.

import base64
from email.policy import default

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_amount
import datetime
from datetime import date


class StudentFeesRegister(models.Model):
    """Student fees Register"""

    _name = "student.fees.register"
    _description = "Student fees Register"

    @api.depends("line_ids")
    def _compute_total_amount(self):
        """Method to compute total amount"""
        for rec in self:
            total_amt = 0.0
            total_amt = sum(line.total for line in rec.line_ids)
            rec.total_amount = total_amt

    name = fields.Char("Name", required=True, help="Enter Name")
    date = fields.Date(
            "Date",
            required=True,
            help="Date of register",
            default=fields.Date.context_today,
    )
    number = fields.Char(
            "Number",
            readonly=True,
            default=lambda self: _("New"),
            help="Sequence number of fee registration form",
    )
    line_ids = fields.One2many(
            "student.payslip", "register_id", "PaySlips", help="Student payslips"
    )
    total_amount = fields.Float(
            "Total", compute="_compute_total_amount", help="Fee total amounts"
    )
    state = fields.Selection(
            [("draft", "Draft"), ("confirm", "Confirm")],
            "State",

            readonly=True,
            default="draft",
            help="State of student fee registration form",
    )
    journal_id = fields.Many2one(
            "account.journal",
            "Journal",
            help="Select Journal",
            required=False,
            default=lambda self: self.env["account.journal"].search(
                    [("type", "=", "sale")], limit=1
            ),
    )
    company_id = fields.Many2one(
            "res.company",
            "Company",
            required=True,
            change_default=True,
            readonly=True,
            default=lambda self: self.env.user.company_id,
            help="Select related company",
    )
    fees_structure = fields.Many2one(
            "student.fees.structure", help="Fee structure")
    standard_id = fields.Many2one(
            "standard.standard", "Class", help="Enter student standard"
    )

    def fees_register_draft(self):
        """Changes the state to draft"""
        self.state = "draft"

    def fees_register_confirm(self):
        """Method to confirm payslip"""
        stud_obj = self.env["student.student"]
        slip_obj = self.env["student.payslip"]
        school_std_obj = self.env["school.standard"]
        for rec in self:
            if not rec.journal_id:
                raise ValidationError(_("Kindly, Select Account Journal!"))
            if not rec.fees_structure:
                raise ValidationError(_("Kindly, Select Fees Structure!"))
            school_std_rec = school_std_obj.search(
                    [("standard_id", "=", rec.standard_id.id)]
            )
            students_rec = stud_obj.search(
                    [
                        ("standard_id", "in", school_std_rec.ids),
                        ("state", "=", "done"),
                    ]
            )
            for stu in students_rec:
                old_slips_rec = slip_obj.search(
                        [("student_id", "=", stu.id), ("date", "=", rec.date)]
                )
                # Check if payslip exist of student
                if slip_obj.search(
                        [("student_id", "=", stu.id), ("date", "=", rec.date)]
                ):
                    raise ValidationError(
                            _("There exists a Fees record for: %s for same " "date.!")
                            % stu.name
                    )
                else:
                    rec.number = self.env["ir.sequence"].next_by_code(
                            "student.fees.register"
                    ) or _("New")
                    res = {
                        "student_id": stu.id,
                        "register_id": rec.id,
                        "name": rec.name,
                        "date": rec.date,
                        "company_id": rec.company_id.id,
                        "currency_id": rec.company_id.currency_id.id or False,
                        "journal_id": rec.journal_id.id,
                        "fees_structure_id": rec.fees_structure.id or False,
                    }
                    slip_rec = slip_obj.create(res)
                    slip_rec.onchange_student()
                    slip_rec.onchange_fees_structure_id()
            # Calculate the amount
            amount = sum([data.total for data in rec.line_ids])
            rec.write({"total_amount": amount, "state": "confirm"})


class StudentTotalsibiling(models.Model):
    """Student sibiling Line"""

    _name = "student.total.sibiling"
    _description = "Student sibiling Line"

    student_id = fields.Many2one(
            "student.student", "Student", required=True, help="Select student"
    )
    name_payment = fields.Char(string="Name")
    amount = fields.Float("Amount", digits=(
        16, 2), readonly="0")
    total_tax = fields.Float("Total Tax", digits=(
        16, 2), help="Total Fee amount", readonly="0")
    total_amount = fields.Float("Total Amount", digits=(
        16, 2), help="Fee amount", readonly="0")
    total_paid = fields.Float("Paid Amount", digits=(
        16, 2), help="Paid Amount", readonly="0")
    total_due = fields.Float("Due Amount", digits=(
        16, 2), help="Due Amoun", readonly="0")
    date = fields.Date("Date", readonly="0")
    sibiling_ids = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip", readonly="0"
    )
    state = fields.Selection(
            [
                ("draft", "Draft"),
                ("confirm", "Confirm"),
                ("pending", "Pending"),
                ("paid", "Paid"),
                ("reverse", "Reverse"),
            ],
            "State",
            readonly=True,
    )

    sibiling_id = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip", readonly="0"
    )

    def create_sibiling_payment(self):
        payslip_studentss = self.env['student.payslip'].create({
            'student_id': self.sibiling_id.id,
            'journal_ids': 1,
            # 'amount': sibiling_id.total_amount_remaining_balance_
            # total_amount_remaining_balance_
        })

        views = self.env.ref('school_fees.view_student_payslip_form')
        return {
            "name": _("Pay Fees"),
            "view_mode": "form",
            "res_model": "student.payslip",
            "view_id": views.id,
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": payslip_studentss.id,
            "context": {},
        }


class StudentTotalBalance(models.Model):
    """Student Balance Line"""

    _name = "student.total.balance"
    _description = "Student Balance Line"

    name_payment = fields.Char(string="Name")
    amount = fields.Float("Amount", digits=(
        16, 2), readonly="0")
    subtotal = fields.Float("Subtotal", digits=(
        16, 2), help="Fee amount")
    total_tax = fields.Char("Tax", digits=(
        16, 2), help="Total Fee amount")
    discount_ids = fields.Many2many('student.discount.fees', string='Discount')
    date = fields.Date("Date")

    balance_id = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip"
    )


class StudentTotalBalanceActivity(models.Model):
    """Student Balance Line"""

    _name = "student.total.balance.activity"
    _description = "Student Balance Line"

    name_payment = fields.Char(string="Name")
    amount = fields.Float("Amount", digits=(
        16, 2), readonly="0")
    subtotal = fields.Float("Subtotal", digits=(
        16, 2), help="Fee amount")
    total_tax = fields.Char("Tax", digits=(
        16, 2), help="Total Fee amount")

    date = fields.Date("Date")

    balance_id_activity = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip"
    )


class StudentTotalBalanceBuss(models.Model):
    """Student Balance Line"""

    _name = "student.total.balance.buss"
    _description = "Student Balance Line"

    name_payment = fields.Char(string="Name")
    amount = fields.Float("Amount", digits=(
        16, 2), readonly="0")
    subtotal = fields.Float("Subtotal", digits=(
        16, 2), help="Fee amount")
    total_tax = fields.Char("Tax", digits=(
        16, 2), help="Total Fee amount")

    date = fields.Date("Date")

    balance_id_buss = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip"
    )


class StudentPayslipLine(models.Model):
    """Student PaySlip Line"""

    _name = "student.payslip.line"
    _description = "Student PaySlip Line"

    name = fields.Char("Name", required=True, help="Payslip")
    code = fields.Char("Code", required=True, help="Payslip code")
    type = fields.Selection(
            [("month", "Monthly"), ("year", "Yearly"), ("range", "Range")],
            "Duration",
            required=True,
            help="Select payslip type",
    )
    tax_ids = fields.Many2many('account.tax', string='taxes')
    amount = fields.Float(digits=(16, 2), help="Fee amount")
    line_ids = fields.One2many(
            "student.payslip.line.line",
            "slipline_id",
            "Calculations",
            help="Payslip line",
    )
    slip_id = fields.Many2one(
            "student.payslip", "Pay Slip", help="Select student payslip"
    )
    description = fields.Text("Description", help="Description",
                              default=lambda self: _('New'))
    company_id = fields.Many2one(
            "res.company",
            "Company",
            change_default=True,
            default=lambda self: self.env.user.company_id,
            help="Related company",
    )
    currency_id = fields.Many2one(
            "res.currency", "Currency", help="Select currency"
    )
    currency_symbol = fields.Char(
            related="currency_id.symbol", string="Symbol", help="Currency Symbol"
    )
    amount = fields.Float("Amount", digits=(
        16, 2), help="Fee amount", readonly="0")
    subtotal = fields.Float("Subtotal", digits=(
        16, 2), help="Fee amount", compute="_compute_amount_total")

    subtotal2 = fields.Float("Subtotal", digits=(
        16, 2), help="Fee amount")

    amount_total = fields.Float("Amount Total", digits=(
        16, 2), help="Total Fee amount", compute="_compute_amount_total")
    account_id = fields.Many2one(
            "account.account", "Account", help="Related account"
    )
    product_id = fields.Many2one("product.product", "Product", required=True)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    total_with_tax = fields.Float("Amount Taxes", digits=(16, 2), help="Total Fee amount",
                                  compute="_compute_amount_total")
    change_subtotal = fields.Boolean(string="Change subtotal", compute="_compute_subtotal_update", default=False)
    # change_subtotal = fields.Boolean(string="Change subtotal",default= False)
    # New
    discount_ids = fields.Many2many('student.discount.fees', string='Discount')

    @api.depends("change_subtotal")
    def _compute_subtotal_update(self):
        for rec in self:
            if rec.change_subtotal:
                rec.subtotal2 = rec.total_with_tax
                rec.change_subtotal = False
            else:
                rec.subtotal2 = rec.total_with_tax
                rec.change_subtotal = True

    @api.onchange("company_id")
    def set_currency_onchange(self):
        """Onchange method to assign currency on change company"""
        for rec in self:
            rec.currency_id = rec.company_id.currency_id.id

    @api.onchange("amount")
    def more_than_tuition_fees(self):
        yearly_ids = self.env['student.yearly.fees'].search(
                [('grade', '=', self.slip_id.student_id.standard_id.id), ('year', '=', self.slip_id.year.id)])
        if self.slip_id.student_id.country_id.id == 192:
            taxess = 1.0
        else:
            taxess = 1.15
        for yearly_id in yearly_ids:
            # raise ValidationError(_("Kindly, The amount more than 'Tuition Fees' ({})").format(yearly_id))
            total_balances = yearly_id.total * taxess
            if self.amount > total_balances:
                raise ValidationError(_("Kindly, The amount more than 'Tuition Fees' ({})").format(total_balances))

    @api.depends("amount", "tax_ids", "discount_ids")
    def _compute_amount_total(self):

        for line in self:
            total = 0
            subtotal = line.amount
            if line.discount_ids:
                for discount in line.discount_ids:
                    subtotal = subtotal * (1 - (discount.discount_amount) / 100.0)
                    # raise ValidationError(_("Subtotal({}),,, \n Discount({}),,,").format(subtotal, discount.discount_amount))
            else:
                subtotal = line.amount
            if line.tax_ids:
                if line.tax_ids.price_include:
                    # line.subtotal = 1000
                    price_tax = line.tax_ids.compute_all(subtotal,
                                                         currency=line.slip_id.currency_id, )
                    line.amount_total = price_tax['total_included']
                    line.subtotal = line.amount_total / 1.15  # - (line.amount_total * (line.tax_ids.amount * 0.01))
                else:
                    price_tax = line.tax_ids.compute_all(subtotal,
                                                         currency=line.slip_id.currency_id, )
                    line.amount_total = price_tax['total_included']
                    line.subtotal = subtotal
                    line.total_with_tax = subtotal * 1.15
            else:
                line.subtotal = subtotal
                line.amount_total = line.subtotal
                line.total_with_tax = line.subtotal


class StudentFeesStructureLine(models.Model):
    """Student Fees Structure Line"""

    _name = "student.fees.structure.line"
    _description = "Student Fees Structure Line"
    _order = "sequence"

    name = fields.Char("Name", required=True, help="Enter fee structure name")
    code = fields.Char("Code", required=True, help="Fee structure code")
    type = fields.Selection(
            [("month", "Monthly"), ("year", "Yearly"), ("range", "Range")],
            "Duration",
            required=True,
            help="Fee structure type",
    )
    product_id = fields.Many2one("product.product", "Product", required=True)
    amount = fields.Float("Amount", digits=(16, 2), help="Fee amount")
    sequence = fields.Integer(
            "Sequence", help="Sequence of fee structure form"
    )
    line_ids = fields.One2many(
            "student.payslip.line.line",
            "slipline1_id",
            "Calculations",
            help="Student payslip line",
    )
    account_id = fields.Many2one("account.account", string="Account")
    company_id = fields.Many2one(
            "res.company",
            "Company",
            change_default=True,
            default=lambda self: self.env.user.company_id,
            help="Related company",
    )
    currency_id = fields.Many2one(
            "res.currency", "Currency", help="Select currency"
    )
    currency_symbol = fields.Char(
            related="currency_id.symbol",
            string="Symbol",
            help="Select currency symbol",
    )
    tax_ids = fields.Many2many('account.tax', string='taxes')

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env["ir.sequence"].next_by_code(
                "student.fees.structure.line"
        )
        res = super(StudentFeesStructureLine, self).create(vals)
        return res

    @api.onchange("company_id")
    def set_currency_company(self):
        for rec in self:
            rec.currency_id = rec.company_id.currency_id.id

    @api.onchange("product_id")
    def onchange_product_id(self):
        for rec in self:
            rec.amount = rec.product_id and rec.product_id.list_price or 0


class StudentFeesStructure(models.Model):
    """Fees structure"""

    _name = "student.fees.structure"
    _description = "Student Fees Structure"

    name = fields.Char("Name", required=True, help="Fee structure name")
    code = fields.Char("Code", required=True, help="Fee structure code")
    line_ids = fields.Many2many(
            "student.fees.structure.line",
            "fees_structure_payslip_rel",
            "fees_id",
            "slip_id",
            "Fees Structure",
            help="Fee structure line",
    )

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "The code of the Fees Structure must be unique !",
        )
    ]


class StudentPayslip(models.Model):
    _name = "student.payslip"
    _description = "Student PaySlip"

    fees_structure_id = fields.Many2one(
            "student.fees.structure",
            "Fees Structure",
            states={"paid": [("readonly", True)]},
            help="Select fee structure",
    )
    kb_note_ps = fields.Text(string='Note', )
    standard_id = fields.Many2one(
            "school.standard", "Class", help="Select school standard"
    )
    division_id = fields.Many2one(
            "standard.division", "Division", help="Select standard division"
    )
    medium_id = fields.Many2one(
            "standard.medium", "Medium", help="Select standard medium"
    )
    country_id = fields.Many2one(
            'res.country', string='Nationality', store=True, related='student_id.country_id')

    father_country_id = fields.Many2one(
            'res.country', string='Father Nationality', store=True, related='student_id.father_country_id')

    mother_country_id = fields.Many2one(
            'res.country', string='Mother Nationality', store=True, related='student_id.mother_country_id')
    register_id = fields.Many2one(
            "student.fees.register", "Register", help="Select student fee register"
    )
    name = fields.Char("Description", help="Payslip name",
                       compute="_compute_description")
    number = fields.Char(
            "Number",
            readonly=True,
            default=lambda self: _("/"),
            copy=False,
            help="Payslip number",
    )
    user_id = fields.Many2one('res.users', string="User", index=True, tracking=2, default=lambda self: self.env.user,
                              readonly=1)
    student_id = fields.Many2one(
            "student.student", "Student", required=True, help="Select student"
    )
    student_mobile = fields.Char(
            related="student_id.mobile", readonly=True, string="Student Phone"
    )
    date = fields.Date(
            "Date",
            readonly=True,
            help="Current Date of payslip",
            default=fields.Date.context_today,
    )

    sibiling_id = fields.Many2one(
            "student.student", "Sibiling")

    @api.onchange("student_id", "sibiling_id")
    def onchange_studentss_ids(self):
        for rec in self:
            for x in rec.student_id.parent_id:
                return {'domain': {'sibiling_id': [('parent_id', '=', x.id), ('id', '!=', rec.student_id.id)]}}

    def create_sibiling_payment(self):
        payslip_studentss = self.env['student.payslip'].create({
            'student_id': self.sibiling_id.id,
            'journal_ids': 1,
        })

        views = self.env.ref('school_fees.view_student_payslip_form')
        return {
            "name": _("Pay Fees"),
            "view_mode": "form",
            "res_model": "student.payslip",
            "view_id": views.id,
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": payslip_studentss.id,
            "context": {},
        }

    @api.onchange("date")
    def date_before(self):
        if self.date < date.today():
            self.date = date.today()
            raise ValidationError(_("Kindly, Select a valid date!"))

    line_ids = fields.One2many(
            "student.payslip.line",
            "slip_id",
            "PaySlip Line",
            copy=False,
            help="Payslips",
    )
    total = fields.Monetary(readonly=True, help="Total Amount")
    line_sibiling_ids = fields.One2many(
            "student.total.sibiling",
            "sibiling_id",
            "sibiling Line",
            copy=False,
            help="sibiling",
    )

    line_balance_ids = fields.One2many(
            "student.total.balance",
            "balance_id",
            "Balance Line",
            copy=False,
            help="Balance",
    )

    line_balance_ids_activity = fields.One2many(
            "student.total.balance.activity",
            "balance_id_activity",
            "Balance Line Activity",
            copy=False
    )

    line_balance_ids_buss = fields.One2many(
            "student.total.balance.buss",
            "balance_id_buss",
            "Balance Line Buss",
            copy=False
    )

    # ('parent_id.name', '=', self.parent_id.name)

    total_balance1 = fields.Monetary("Total Balance")
    total_tax1 = fields.Monetary("Total Tax")
    total_balance_discount1 = fields.Monetary("Total Balance Discount")
    total_amount_paid_balance_1 = fields.Monetary("Total paid")
    total_amount_remaining_balance_1 = fields.Monetary("Total remaining")
    # is_invoice_balance2 = fields.Boolean("Is Invoice Paid", compute="compute_Is_invoice_paid2", default= True)
    total_balance = fields.Monetary("Total Balance", readonly=True, compute="_total_balance_all")
    total_balance_discount = fields.Monetary("Total Balance Discount", readonly=True)
    total_amount_paid_balance_ = fields.Monetary("Total paid", readonly=True)
    total_amount_remaining_balance_ = fields.Monetary("Total remaining", readonly=True, compute="_total_remaining_all")

    @api.depends('total_balance')
    def _total_balance_all(self):
        yearly_ids = self.env['student.yearly.fees'].search(
                [('grade', '=', self.student_id.standard_id.id), ('year', '=', self.year.id)])
        self.total_balance = 0
        total_balances = 0
        taxess = 1.0
        self.total_balance_discount = 0
        if self.student_id.special_discount != 0:
            pass
        elif self.have_siblings == 1:
            self.student_id.special_discount = 5
        elif self.have_siblings > 1:
            self.student_id.special_discount = 10
        if self.student_id.country_id.id == 192:
            taxess = 1.0
        else:
            taxess = 1.15
        for yearly_id in yearly_ids:
            total_balances = yearly_id.total
            self.total_balance = total_balances
            if self.student_id.discount_ids:
                for xdiscount in self.student_id.discount_ids:
                    discount = total_balances * (xdiscount.discount_amount * 0.01)
                    total_balances = total_balances - discount
                    # self.total_tax = total_balances * taxess
                total_balances = total_balances * taxess
                self.total_balance_discount = total_balances
            else:
                self.total_balance_discount = self.total_balance * taxess
                # self.toteal_tax = self.total_balance * taxess
            # if self.student_id.special_discount:
            #     self.total_balance_discount = total_balances - ((total_balances) * (self.student_id.special_discount * 0.01))
            # else:
            #     self.total_balance_discount = self.total_balance * taxess

    @api.depends('total_amount_remaining_balance_')
    def _total_remaining_all(self):
        # if self.total_balance:
        self.total_amount_remaining_balance_ = self.total_balance_discount - self.total_amount_paid_balance_

    is_reverse = fields.Boolean("Is Reverse", compute="_create_reverse")

    @api.depends('is_reverse')
    def _create_reverse(self):
        if self.move_id.reversal_move_id:
            for xmm in self.move_id.reversal_move_id:
                if xmm.state == 'posted':
                    self.state = 'reverse'
                    self.is_reverse = True
                else:
                    self.is_reverse = False
        else:
            self.is_reverse = False

    is_invoice_balance2 = fields.Boolean("Is Invoice Paid", compute="_create_payment_balance")

    @api.depends('is_invoice_balance2')
    def _create_payment_balance(self):
        sale_order_line = []
        total_amount_paid_balance = 0
        tax = 0
        balance = 0
        total_balance = 0
        balance_ids = self.env['student.payslip'].search([('student_id', '=', self.student_id.id)])
        # raise ValidationError(_(yearly_ids.total))
        self.env['student.total.balance'].search([('balance_id', '=', self.id)]).unlink()
        bs = []
        for balance_idss in balance_ids:

            for balance_idsss in balance_idss:

                if balance_idsss.state == 'paid' and balance_idsss.year.id == self.year.id:
                    for balancess in balance_idsss.line_ids:
                        if balancess.name == 'School Fees':
                            if balancess.tax_ids.amount != 0:
                                tax = 1.15
                                balance = balancess.subtotal * tax
                                total_balance = self.total_balance * tax
                            else:
                                tax = 0
                                balance = balancess.subtotal
                                total_balance = self.total_balance
                            if balancess.discount_ids:
                                for bx in balancess.discount_ids:
                                    bs.append(bx.id)
                            sale_order_line.append(self.env['student.total.balance'].create({
                                'balance_id': self.id,
                                'name_payment': balancess.name,
                                'date': balance_idsss.date,
                                'amount': balancess.amount,
                                # 'discount_ids': [(6, 0, bs)],
                                'total_tax': balancess.tax_ids.amount,
                                'subtotal': balance,
                            })
                            )
                            total_amount_paid_balance += balance
                            self.is_invoice_balance2 = True

                        else:
                            #     pass
                            self.is_invoice_balance2 = False
                else:
                    #     pass
                    self.is_invoice_balance2 = False
        self.total_amount_paid_balance_ = total_amount_paid_balance
        self.total_balance = total_balance
        # else:
        #     pass

    # Sibiling Balance

    is_invoice_balance_sibiling = fields.Boolean("Is Invoice Paid", compute="_create_payment_balance_sibiling")

    @api.depends('is_invoice_balance_sibiling')
    def _create_payment_balance_sibiling(self):
        siblings_line = []
        total_amount_paid_balance = 0
        # student_id = self.env['student.student'].search([('id','=',self.student_id.id)])
        # if not self.line_sibiling_ids:
        # for student_ids in student_id:
        self.env['student.total.sibiling'].search([('sibiling_id', '=', self.id)]).unlink()
        for siblings in self.student_id.siblings_ids:
            student_siblings_id = self.env['student.payslip'].search(
                    [('student_id', '=', siblings.student_sibling_id.id)])
            # raise ValidationError(_(siblings.student_sibling_id))

            for payslip in student_siblings_id:
                if payslip.year.id == self.year.id:
                    siblings_line.append(self.env['student.total.sibiling'].create({
                        'student_id': payslip.student_id.id,
                        'amount': payslip.total_amount,
                        'total_tax': payslip.tax_amount,
                        'total_amount': payslip.total,
                        'date': payslip.date,
                        'total_due': payslip.due_amount,
                        'total_paid': payslip.paid_amount,
                        'sibiling_ids': payslip.id,
                        'state': payslip.state,
                        'sibiling_id': self.id,
                    })
                    )
        self.is_invoice_balance_sibiling = False
        # else:
        # self.is_invoice_balance_sibiling = True

        # balance_ids = self.env['student.payslip'].search([('student_id','=', self.student_id.id)])
        # # raise ValidationError(_(yearly_ids.total))
        # self.env['student.total.balance.activity'].search([('balance_id_activity','=', self.id)]).unlink()
        # for balance_idss in balance_ids:

        #     for balance_idsss in balance_idss:

        #         if balance_idsss.state == 'paid':
        #             for balancess in balance_idsss.line_ids:
        #                 if balancess.name == 'activity fee':
        #                     sale_order_line.append(self.env['student.total.balance.activity'].create({
        #                             'balance_id_activity': self.id,
        #                             'name_payment': balancess.name,
        #                             'date': balance_idsss.date,
        #                             'amount': balancess.amount,
        #                             'total_tax': balancess.tax_ids.amount,
        #                             'subtotal': balancess.subtotal,
        #                             })
        #                     )
        #                     total_amount_paid_balance += balancess.amount
        #                     self.is_invoice_balance_activity = True

        #                 else:
        #                 #     pass
        #                     self.is_invoice_balance_activity = False
        #         else:
        #         #     pass
        #             self.is_invoice_balance_activity = False

    # Activity Balance
    total_balance_activity = fields.Monetary("Total Balance", readonly=True, compute="_total_balance_all_activity")
    total_amount_paid_balance_activity = fields.Monetary("Total paid", readonly=True)
    total_amount_remaining_balance_activity = fields.Monetary("Total remaining", readonly=True,
                                                              compute="_total_remaining_all_activity")

    @api.depends('total_balance_activity')
    def _total_balance_all_activity(self):
        yearly_ids = self.env['student.yearly.fees'].search([('grade', '=', self.student_id.standard_id.id)])
        for yearly_id in yearly_ids:
            self.total_balance_activity = yearly_id.total

    @api.depends('total_amount_paid_balance_activity')
    def _total_remaining_all_activity(self):
        self.total_amount_remaining_balance_activity = self.total_balance_activity - self.total_amount_paid_balance_activity

    is_invoice_balance_activity = fields.Boolean("Is Invoice Paid", compute="_create_payment_balance_activity")

    @api.depends('is_invoice_balance_activity')
    def _create_payment_balance_activity(self):
        sale_order_line = []
        total_amount_paid_balance = 0
        subtotal_12 = 0
        balance_ids = self.env['student.payslip'].search([('student_id', '=', self.student_id.id)])
        # raise ValidationError(_(yearly_ids.total))
        self.env['student.total.balance.activity'].search([('balance_id_activity', '=', self.id)]).unlink()
        for balance_idss in balance_ids:

            for balance_idsss in balance_idss:

                if balance_idsss.state == 'paid' and balance_idsss.year.id == self.year.id:
                    for balancess in balance_idsss.line_ids:
                        if balancess.name == 'activity fee' or balancess.name == 'id card':
                            if balancess.tax_ids.amount == 15.0:
                                subtotal_12 = balancess.subtotal * 1.15
                            else:
                                subtotal_12 = balancess.subtotal
                            sale_order_line.append(self.env['student.total.balance.activity'].create({
                                'balance_id_activity': self.id,
                                'name_payment': balancess.name,
                                'date': balance_idsss.date,
                                'amount': balancess.amount,
                                'total_tax': balancess.tax_ids.amount,
                                'subtotal': subtotal_12,
                            })
                            )
                            total_amount_paid_balance += subtotal_12
                            self.is_invoice_balance_activity = True

                        else:
                            #     pass
                            self.is_invoice_balance_activity = False
                else:
                    #     pass
                    self.is_invoice_balance_activity = False
        self.total_amount_paid_balance_activity = total_amount_paid_balance
        # else:
        #     pass

        # Buss Balance

    total_balance_buss = fields.Monetary("Total Balance", readonly=True, compute="_total_balance_all_buss")
    total_amount_paid_balance_buss = fields.Monetary("Total paid", readonly=True)
    total_amount_remaining_balance_buss = fields.Monetary("Total remaining", readonly=True,
                                                          compute="_total_remaining_all_buss")

    @api.depends('total_balance_buss')
    def _total_balance_all_buss(self):
        yearly_ids = self.env['student.yearly.fees'].search([('grade', '=', self.student_id.standard_id.id)])
        for yearly_id in yearly_ids:
            self.total_balance_buss = yearly_id.total

    @api.depends('total_amount_paid_balance_buss')
    def _total_remaining_all_buss(self):
        self.total_amount_remaining_balance_buss = self.total_balance_buss - self.total_amount_paid_balance_buss

    is_invoice_balance_buss = fields.Boolean("Is Invoice Paid", compute="_create_payment_balance_buss")

    @api.depends('is_invoice_balance_buss')
    def _create_payment_balance_buss(self):
        sale_order_line = []
        total_amount_paid_balance = 0
        balance_ids = self.env['student.payslip'].search([('student_id', '=', self.student_id.id)])
        # raise ValidationError(_(yearly_ids.total))
        self.env['student.total.balance.buss'].search([('balance_id_buss', '=', self.id)]).unlink()
        for balance_idss in balance_ids:

            for balance_idsss in balance_idss:

                if balance_idsss.state == 'paid' and balance_idsss.year.id == self.year.id:
                    for balancess in balance_idsss.line_ids:
                        if balancess.name == 'Trans':
                            if balancess.tax_ids.amount == 15.0:
                                subtotal_buss = balancess.subtotal * 1.15
                            else:
                                subtotal_buss = balancess.subtotal
                            sale_order_line.append(self.env['student.total.balance.buss'].create({
                                'balance_id_buss': self.id,
                                'name_payment': balancess.name,
                                'date': balance_idsss.date,
                                'amount': balancess.amount,
                                'total_tax': balancess.tax_ids.amount,
                                'subtotal': subtotal_buss,
                            })
                            )
                            total_amount_paid_balance += subtotal_buss
                            self.is_invoice_balance_buss = True

                        else:
                            #     pass
                            self.is_invoice_balance_buss = False
                else:
                    #     pass
                    self.is_invoice_balance_buss = False
        self.total_amount_paid_balance_buss = total_amount_paid_balance
        # else:
        #     pass

    total = fields.Monetary("Total", readonly=True,
                            help="Total Amount", compute="_amount_all")
    state = fields.Selection(
            [
                ("draft", "Draft"),
                ("confirm", "Confirm"),
                ("pending", "Pending"),
                ("paid", "Paid"),
            ],
            readonly=True,
            default="draft",
            help="State of the student payslip",
    )
    journal_id = fields.Many2one(
            "account.journal",
            "Journal",
            required=False,
            help="Select journal for account",
    )

    paid_amount = fields.Monetary(
            "Paid Amount", help="Amount Paid", compute='_compute_amount')
    total_amount = fields.Monetary(
            "Total Amount", help="Total Amount", compute='_amount_all')
    tax_amount = fields.Monetary(
            "Tax Amount", help="Tax Amount", compute='_amount_all')
    due_amount = fields.Monetary(
            "Due Amount", help="Amount Remaining", compute='_compute_amount')
    currency_id = fields.Many2one(related='company_id.currency_id', string="Currency",
                                  help="Selelct currency")
    currency_symbol = fields.Char(
            related="currency_id.symbol", string="Symbol", help="Currency symbol"
    )
    move_id = fields.Many2one(
            "account.move",
            "Journal Entry",
            readonly=True,
            ondelete="restrict",
            copy=False,
            help="Link to the automatically generated Journal Items.",
    )
    partner_id = fields.Many2one(
            "res.partner",
            readonly=True,
            related="move_id.partner_id"
    )
    payment_date = fields.Date(
            "Payment Date",
            readonly=True,
            states={"draft": [("readonly", False)]},
            help="Keep empty to use the current date",
    )
    type = fields.Selection(
            [
                ("out_invoice", "Customer Invoice"),
                ("in_invoice", "Supplier Invoice"),
                ("out_refund", "Customer Refund"),
                ("in_refund", "Supplier Refund"),
            ],
            "Type",
            required=True,
            change_default=True,
            default="out_invoice",
            help="Payslip type",
    )
    company_id = fields.Many2one(
            "res.company",
            "Company",
            required=True,
            change_default=True,
            readonly=True,
            default=lambda self: self.env.user.company_id,
            help="Related company",
    )
    total_invoiced = fields.Integer(compute='_get_invoiced', readonly=True)
    # is_invoice_paid = fields.Boolean("Is Invoice Paid", default=False,compute="_compute_Is_invoice_paid")
    have_siblings = fields.Integer('Have Siblings', default=0)
    student_id_no = fields.Char(related="student_id.pid")
    payment_types_id = fields.Many2one(
            "ems.payment.types", string="Payment Types")

    _sql_constraints = [
        (
            "code_uniq",
            "unique(student_id,date,state)",
            "The code of the Fees Structure must be unique !",
        )
    ]

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in Student'''
        res = self.env['academic.year'].search([('current', '=', True)])
        if not res:
            raise ValidationError(_(
                    "There is no current Academic Year defined!\
Please contact Administator!"))
        return res.id

    year = fields.Many2one('academic.year', 'Academic Year', readonly=False,
                           default=check_current_year,
                           help='Select academic year')

    @api.depends('line_ids.amount')
    def _amount_all(self):
        """
        Compute the total amounts of the payslip.
        """
        for payslip in self:
            total = 0.0
            paid_amount = 0.0
            total_amount = 0.0
            for line in payslip.line_ids:
                # if line.tax_ids:
                #     if line.tax_ids.price_include:
                #         total += line.amount_total
                #         total_amount += line.subtotal
                #     else:
                #         total += line.amount_total
                #         total_amount += line.subtotal
                # else:
                total += line.amount_total
                total_amount += line.subtotal
            payslip.update({
                'total': total,
                'total_amount': total_amount,
                'tax_amount': total - total_amount,
                'due_amount': total - paid_amount,
            })

    @api.depends('move_id.payment_state')
    def _compute_amount(self):
        for payslip in self:

            # total = 0
            paid_amount = 0.0
            due_amount = 0.0
            # state = ''
            if payslip.move_id.payment_state == 'paid':
                # state = 'paid'
                if payslip.move_id:
                    paid_amount += payslip.total
                    due_amount = due_amount
                elif not payslip.move_id:
                    paid_amount = paid_amount
                    due_amount += payslip.total
            else:
                # paid_amount = paid_amount
                due_amount += payslip.total

            payslip.paid_amount = paid_amount
            payslip.due_amount = due_amount
            # if state:
            #     payslip.state = state

    def _get_invoiced(self):
        for payslip in self:
            inv = self.env['account.move'].search(
                    [('student_payslip_id', '=', payslip.id)])

            payslip.total_invoiced = len(inv)

    @api.onchange("student_id")
    def onchange_student(self):
        """Method to get standard , division , medium of student selected"""
        if self.student_id and self.student_id.standard_id:
            self.standard_id = self.student_id.standard_id.id or False
            self.division_id = (
                    self.student_id.standard_id.division_id.id or False
            )
            self.medium_id = self.student_id.medium_id or False
            self.have_siblings = len(self.student_id.siblings_ids)

            # BALANCE
            yearly_ids = self.env['student.yearly.fees'].search(
                    [('grade', '=', self.student_id.standard_id.id), ('year', '=', self.year.id)])
            self.total_balance1 = 0
            total_balances = 0
            taxess = 1.0
            taxses = 0
            self.total_balance_discount1 = 0
            maxdate = self.student_id.admission_date
            # if self.student_id.sibilings_ids:
            # for x in self.student_id.sibilings_ids:
            #     if maxdate < x.student_sibling_id.admission_date:
            #         maxdate = x.student_sibling_id.admission_date
            if self.student_id.special_discount != 0:
                pass
            elif self.have_siblings == 1:
                self.student_id.special_discount = 5
            elif self.have_siblings > 1:
                self.student_id.special_discount = 10
            if self.student_id.country_id.id == 192:
                taxess = 1.0
                taxses = 0

            else:
                taxess = 1.15
                taxses = 0.15
            for yearly_id in yearly_ids:
                total_balances = yearly_id.total
                self.total_balance1 = total_balances
                if self.student_id.discount_ids:
                    for xdiscount in self.student_id.discount_ids:
                        discount = total_balances * (xdiscount.discount_amount * 0.01)
                        total_balances = total_balances - discount

                    self.total_tax1 = total_balances * taxses
                    total_balances = total_balances + self.total_tax1
                    # raise ValidationError(_(total_balances))
                    self.total_balance_discount1 = total_balances
                else:
                    self.total_balance_discount1 = self.total_balance1 * taxess
                    self.total_tax1 = self.total_balance1 * taxses

            # BALANCE 2e
            sale_order_line = []
            total_amount_paid_balance = 0
            tax = 0
            balance = 0
            total_balance = 0
            balance_ids = self.env['student.payslip'].search([('student_id', '=', self.student_id.id)])
            # raise ValidationError(_(yearly_ids.total))
            self.env['student.total.balance'].search([('balance_id', '=', self.id)]).unlink()
            for balance_idss in balance_ids:

                for balance_idsss in balance_idss:

                    if balance_idsss.state == 'paid' and balance_idsss.year.id == self.year.id:
                        for balancess in balance_idsss.line_ids:
                            if balancess.name == 'School Fees':
                                if balancess.tax_ids.amount != 0:
                                    tax = 1.15
                                    balance = balancess.subtotal * tax
                                    total_balance = self.total_balance * tax
                                else:
                                    tax = 0
                                    balance = balancess.subtotal
                                    total_balance = self.total_balance

                                total_amount_paid_balance += balance

            self.total_amount_paid_balance_1 = total_amount_paid_balance
            # self.total_balance1 = total_balance

            self.total_amount_remaining_balance_1 = self.total_balance_discount1 - self.total_amount_paid_balance_1

    def unlink(self):
        """Inherited unlink method to check state at the record deletion"""
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(
                        _("You can delete record in unconfirm state only!")
                )
        return super(StudentPayslip, self).unlink()

    # @api.depends('student_id')
    # def _compute_name(self):
    #     for rec in self:
    #         rec.name = "fees from" + rec.student_id
    #         if rec.state != "draft":
    #             raise ValidationError(
    #                     _("You can delete record in unconfirm state only!")
    #             )
    #     return super(StudentPayslip, self).unlink()
    @api.onchange("journal_id")
    def onchange_journal_id(self):
        """Method to get currency from journal"""
        for rec in self:
            journal = rec.journal_id
            currency_id = (
                    journal
                    and journal.currency_id
                    and journal.currency_id.id
                    or journal.company_id.currency_id.id
            )
            rec.currency_id = currency_id

    @api.depends("student_id.name")
    def _compute_description(self):
        for rec in self:
            rec.name = "fees from %s" % rec.student_id.name

    @api.onchange("fees_structure_id")
    def onchange_fees_structure_id(self):
        """"Method to  change respective fees structure details on changing of fees_structure_id"""
        for rec in self:
            lines = [(5, 0, 0)]
            ids = []
            for data in rec.fees_structure_id.line_ids or []:
                if data.name == 'School Fees':
                    ids.append(1)
                    yearlyfees = self.env['student.yearly.fees'].search(
                            [('grade', '=', self.student_id.standard_id.id), ('year', '=', self.year.id)], limit=1)
                    discount = rec.student_id.total_discount
                    payslip = self.env['student.payslip'].search(
                            [('student_id', '=', rec.student_id.id), ('year', '=', rec.year.id)])
                    reg = 0
                    for payslips in payslip:
                        if payslips.fees_structure_id.id == 2:
                            reg = payslips.total_amount

                    amount = yearlyfees.total - reg
                    if rec.have_siblings > 0:
                        ids.append(5)

                    for di in rec.student_id.discount_ids:
                        ids.append(di.id)


                else:
                    discount = 0
                    amount = data.amount

                if data.name == "School Fees":
                    if rec.student_id.country_id.code == "SA":
                        line_vals = {
                            "slip_id": rec.id,
                            "name": data.name,
                            "code": data.code,
                            "type": data.type,
                            "account_id": data.account_id.id,
                            # "tax_ids": [(6, 0, data.tax_ids.ids)],
                            'discount_ids': [(6, 0, ids)],
                            "amount": amount,
                            "currency_id": data.currency_id.id or False,
                            "currency_symbol": data.currency_symbol or False,
                        }
                    else:
                        line_vals = {
                            "slip_id": rec.id,
                            "name": data.name,
                            "code": data.code,
                            "type": data.type,
                            "account_id": data.account_id.id,
                            "tax_ids": [(6, 0, data.tax_ids.ids)],
                            'discount_ids': [(6, 0, ids)],
                            "amount": amount,
                            "currency_id": data.currency_id.id or False,
                            "currency_symbol": data.currency_symbol or False,
                        }

                elif data.name == "Registration Fees" and rec.student_id.nationality_id.id == 192:

                    line_vals = {
                        "slip_id": rec.id,
                        "name": data.name,
                        "code": data.code,
                        "type": data.type,
                        "account_id": data.account_id.id,
                        'discount_ids': [(6, 0, ids)],
                        # "tax_ids":False ,
                        "amount": amount,
                        "currency_id": data.currency_id.id or False,
                        "currency_symbol": data.currency_symbol or False,
                    }

                # or data.name == "Regeisterion Fees"
                else:

                    line_vals = {
                        "slip_id": rec.id,
                        "name": data.name,
                        "code": data.code,
                        "type": data.type,
                        "account_id": data.account_id.id,
                        # 'discount_ids': [(6, 0, [1])],
                        "tax_ids": [(6, 0, data.tax_ids.ids)],
                        "amount": amount,
                        "currency_id": data.currency_id.id or False,
                        "currency_symbol": data.currency_symbol or False,
                    }
                lines.append((0, 0, line_vals))
            rec.write({"line_ids": lines})
            print(rec)

    def _update_student_vals(self, vals):
        student_rec = self.env["student.student"].browse(vals.get("student_id"))
        vals.update(
                {
                    "standard_id": student_rec.standard_id.id,
                    "division_id": student_rec.standard_id.division_id.id,
                    "medium_id": student_rec.medium_id.id,
                }
        )

    @api.model
    def create(self, vals):
        """Inherited create method to assign values from student model"""
        if vals.get("student_id"):
            self._update_student_vals(vals)
        return super(StudentPayslip, self).create(vals)

    def write(self, vals):
        """Inherited write method to update values from student model"""
        if vals.get("student_id"):
            self._update_student_vals(vals)
            if self.state != 'paid' and vals.get("state") == 'paid':
                self._paid_payslip_mail()
        return super(StudentPayslip, self).write(vals)

    def _paid_payslip_mail(self):
        template = self.env.ref(
                'school_fees.mail_template_student_fees_paid_send_mail', raise_if_not_found=True)
        if self.move_id:
            pdf = self.env.ref('account.account_invoices')._render_qweb_pdf(
                    self.move_id.ids)[0]
            pdf = base64.b64encode(pdf)
            attach_id = self.env["ir.attachment"].sudo().create(
                    {
                        "type": "binary",
                        "name": self.move_id.name,
                        "datas": pdf,
                        "res_model": "account.move",
                        "res_id": self.move_id.id,
                        "mimetype": "application/pdf"
                    }
            ).id
            template.sudo().write({"attachment_ids": [(6, 0, [attach_id])]})
        # template.
        email_values = {'email_to': self.student_id.email,
                        'subject': 'Fees Payment Confirmation', 'auto_delete': False}
        template.send_mail(self.id, force_send=True, email_values=email_values)  # , raise_exception=True
        return True

    def payslip_draft(self):
        """Change state to draft"""
        self.state = "draft"

    def payslip_paid(self):
        """Change state to paid"""
        self.state = "paid"

    def payslip_confirm(self):
        """Method to confirm payslip"""
        for rec in self:
            if not rec.student_id.email:
                raise ValidationError(_("Please add student's email address"))
            if not rec.journal_id:
                raise ValidationError(_("Kindly, Select Account Journal!"))
            if not rec.fees_structure_id:
                raise ValidationError(_("Kindly, Select Fees Structure!"))
            lines = []
            for data in rec.fees_structure_id.line_ids or []:
                line_vals = {
                    "slip_id": rec.id,
                    "product_id": data.product_id.id,
                    "name": data.name,
                    "code": data.code,
                    "type": data.type,
                    "account_id": data.account_id.id,
                    "amount": data.amount,
                    "currency_id": data.currency_id.id or False,
                    "currency_symbol": data.currency_symbol or False,
                }
                lines.append((0, 0, line_vals))
            rec.write({"line_ids": lines})
            # Compute amount
            amount = 0
            amount = sum(data.amount for data in rec.line_ids)
            rec.register_id.write({"total_amount": rec.total})
            rec.write(
                    {
                        "total": amount,
                        "state": "confirm",
                        "due_amount": amount,
                        "currency_id": rec.company_id.currency_id.id or False,
                    }
            )
            template = (
                self.env["mail.template"]
                .sudo()
                .search([("name", "ilike", "Fees Reminder")], limit=1)
            )
            if template:
                for user in rec.student_id.parent_id:
                    subject = _("Fees Reminder")
                    if user.email:
                        body = _(
                                """
                            <div>
                                <p>Dear """
                                + str(user.display_name)
                                + """,
                            <br/><br/>
                            We are getting in touch as school fees due on """
                                + str(rec.date)
                                + """ remain unpaid for """
                                + str(rec.student_id.display_name)
                                + """.
                            <br/><br/>
                            We kindly ask that you arrange to pay the """
                                + str(rec.due_amount)
                                + """ balance as soon as possible.
                            <br/><br/>
                            Thank You.
                        </div>"""
                        )
                        template.send_mail(
                                rec.id,
                                email_values={
                                    "email_from": self.env.user.email or "",
                                    "email_to": user.email,
                                    "subject": subject,
                                    "body_html": body,
                                },
                                force_send=True,
                        )

    def invoice_view(self):
        """View number of invoice of student"""
        invoice_obj = self.env["account.move"]
        for rec in self:
            invoices_rec = invoice_obj.search([("student_payslip_id", "=", rec.id)])
            action = rec.env.ref("account.action_move_out_invoice_type").read()[0]
            if len(invoices_rec) > 1:
                action["domain"] = [("id", "in", invoices_rec.ids)]
            elif len(invoices_rec) == 1:
                action["views"] = [(rec.env.ref("account.view_move_form").id, "form")]
                action["res_id"] = invoices_rec.ids[0]
            else:
                action = {"type": "ir.actions.act_window_close"}
        return action

    def action_move_create(self):
        cur_obj = self.env["res.currency"]
        move_obj = self.env["account.move"]
        move_line_obj = self.env["account.move.line"]
        for fees in self:
            if not fees.journal_id.sequence_id:
                raise ValidationError(
                        _(
                                "Please define sequence on the journal related to "
                                "this invoice."
                        )
                )
            # field 'centralisation' from account.journal
            #  is deprecated field since v9
            if fees.move_id:
                continue
            ctx = self._context.copy()
            ctx.update({"lang": fees.student_id.lang})
            if not fees.payment_date:
                self.write([fees.id], {"payment_date": fields.Date.today()})
            company_currency = fees.company_id.currency_id.id
            diff_currency_p = fees.currency_id.id != company_currency
            current_currency = (
                    fees.currency_id and fees.currency_id.id or company_currency
            )
            account_id = False
            comapny_ac_id = False
            if fees.type in ("in_invoice", "out_refund"):
                account_id = fees.student_id.property_account_payable.id
                cmpy_id = fees.company_id.partner_id
                comapny_ac_id = cmpy_id.property_account_receivable.id
            elif fees.type in ("out_invoice", "in_refund"):
                account_id = fees.student_id.property_account_receivable.id
                cmp_id = fees.company_id.partner_id
                comapny_ac_id = cmp_id.property_account_payable.id
            move = {
                "ref": fees.name,
                "journal_id": fees.journal_id.id,
                "date": fees.payment_date or fields.Date.today(),
            }
            ctx.update({"company_id": fees.company_id.id})
            move_id = move_obj.create(move)
            context_multi_currency = self._context.copy()
            context_multi_currency.update({"date": fields.Date.today()})
            debit = 0.0
            credit = 0.0
            if fees.type in ("in_invoice", "out_refund"):
                # compute method from res.currency is deprecated
                #    since v12 and replaced with _convert
                credit = cur_obj._convert(
                        fees.total, company_currency, fees.company_id, self.date
                )
            elif fees.type in ("out_invoice", "in_refund"):
                debit = cur_obj._convert(
                        fees.total, company_currency, fees.company_id, self.date
                )
            if debit < 0:
                credit = -debit
                debit = 0.0
            if credit < 0:
                debit = -credit
                credit = 0.0
            sign = debit - credit < 0 and -1 or 1
            cr_id = diff_currency_p and current_currency or False
            am_cr = diff_currency_p and sign * fees.total or 0.0
            date = fees.payment_date or fields.Date.today()
            move_line = {
                "name": fees.name or "/",
                "move_id": move_id,
                "debit": debit,
                "credit": credit,
                "account_id": account_id,
                "journal_id": fees.journal_id.id,
                "parent_id": fees.student_id.parent_id.id,
                "currency_id": cr_id,
                "amount_currency": am_cr,
                "date": date,
            }
            move_line_obj.create(move_line)
            cr_id = diff_currency_p and current_currency or False
            move_line = {
                "name": fees.name or "/",
                "move_id": move_id,
                "debit": credit,
                "credit": debit,
                "account_id": comapny_ac_id,
                "journal_id": fees.journal_id.id,
                "parent_id": fees.student_id.parent_id.id,
                "currency_id": cr_id,
                "amount_currency": am_cr,
                "date": date,
            }
            move_line_obj.create(move_line)
            fees.write({"move_id": move_id})
            move_obj.action_post([move_id])

    # def student_pay_fees(self):
    #     """Generate invoice of student fee"""
    #     sequence_obj = self.env["ir.sequence"]
    #     ctx = self._context.copy()
    #     for rec in self:
    #         if rec.number == "/":
    #             rec.number = sequence_obj.next_by_code("student.payslip") or _("New")
    #         rec.state = "pending"
    #         partner = rec.student_id and rec.student_id.partner_id
    #         vals = {
    #             "partner_id": partner.id,
    #             "invoice_date": rec.date,
    #             "journal_id": rec.journal_id.id,
    #             "name": rec.number,
    #             "student_payslip_id": rec.id,
    #             "move_type": "out_invoice",
    #         }
    #         invoice_line = []
    #         for line in rec.line_ids:
    #             #     replaced / deprecated fields of v13:
    #             #     default_debit_account_id,
    #             #     default_credit_account_id from account.journal
    #             acc_id = rec.journal_id.default_account_id.id
    #             if line.account_id.id:
    #                 acc_id = line.account_id.id
    #             else:
    #                 acc_id = rec.journal_id.default_account_id.id
    #             invoice_line_vals = {
    #                 "name": line.name,
    #                 "product_id": line.product_id.id,
    #                 "account_id": acc_id,
    #                 "quantity": 1.000,
    #                 "discount": line.discount or 0.00,
    #                 "price_unit": line.amount,
    #                 "tax_ids": [(6, 0, line.tax_ids.ids)]
    #             }
    #             invoice_line.append((0, 0, invoice_line_vals))
    #         vals.update({"invoice_line_ids": invoice_line})
    #         # creates invoice
    #         account_invoice_id = self.env["account.move"].create(vals)
    #         rec.write({'move_id': account_invoice_id.id})
    #         account_invoice_id.action_post()
    #         if ctx.get("is_paid", False):
    #             vals = {'journal_id': ctx.get("journal_id", False),
    #                     'amount': account_invoice_id.amount_total,
    #                     'payment_date': account_invoice_id.invoice_date,
    #                     'communication': account_invoice_id.name,
    #                     'payment_type': 'inbound',
    #                     }
    #             register_payment = self.env['account.payment.register']. \
    #                 with_context(active_id=account_invoice_id.id,
    #                              active_ids=[account_invoice_id.id],
    #                              active_model='account.move',
    #                              dont_redirect_to_payments=True).create(vals)
    #             register_payment._compute_payment_method_id()
    #             register_payment.with_context(
    #                     dont_redirect_to_payments=True).action_create_payments()
    #             rec.write({'payment_date': register_payment.payment_date})
    #         invoice_obj = self.env.ref("account.view_move_form")
    #         return {
    #             "name": _("Pay Fees"),
    #             "view_mode": "form",
    #             "res_model": "account.move",
    #             "view_id": invoice_obj.id,
    #             "type": "ir.actions.act_window",
    #             "nodestroy": True,
    #             "target": "current",
    #             "res_id": account_invoice_id.id,
    #             "context": {},
    #         }
    def student_pay_fees(self):
        """Generate invoice of student fee"""
        sequence_obj = self.env["ir.sequence"]
        for rec in self:
            if rec.number == "/":
                rec.number = sequence_obj.next_by_code("student.payslip") or _("New")
            rec.state = "pending"
            partner = rec.student_id and rec.student_id.partner_id
            vals = {
                "partner_id": partner.id,
                "invoice_date": rec.date,
                "journal_id": rec.journal_id.id,
                "name": rec.number,
                "student_payslip_id": rec.id,
                "move_type": "out_invoice",
            }
            invoice_line = []
            for line in rec.line_ids:
                #     replaced / deprecated fields of v13:
                #     default_debit_account_id,
                #     default_credit_account_id from account.journal
                acc_id = rec.journal_id.default_account_id.id
                if line.account_id.id:
                    acc_id = line.account_id.id
                invoice_line_vals = {
                    "name": line.name,
                    "product_id": line.product_id.id,
                    "account_id": acc_id,
                    "quantity": 1.000,
                    "price_unit": line.amount,
                }
                invoice_line.append((0, 0, invoice_line_vals))
            vals.update({"invoice_line_ids": invoice_line})
            # creates invoice
            account_invoice_id = self.env["account.move"].create(vals)
            invoice_obj = self.env.ref("account.view_move_form")
            return {
                "name": _("Pay Fees"),
                "view_mode": "form",
                "res_model": "account.move",
                "view_id": invoice_obj.id,
                "type": "ir.actions.act_window",
                "nodestroy": True,
                "target": "current",
                "res_id": account_invoice_id.id,
                "context": {},
            }

    def student_pay_fees_new(self):
        """Generate invoice of student fee"""
        sequence_obj = self.env["ir.sequence"]
        ctx = self._context.copy()
        for rec in self:
            if rec.number == "/":
                rec.number = sequence_obj.next_by_code("student.payslip")
                # or _(
                #     "INV/0001"
                # )
            rec.state = "paid"
            partner = rec.student_id and rec.student_id.partner_id
            vals = {
                "partner_id": partner.id,
                "invoice_date": rec.date,
                "journal_id": rec.journal_id.id,
                "name": rec.number,
                "student_id": rec.student_id,
                "student_payslip_id": rec.id,
                "move_type": "out_invoice",
            }
            invoice_line = []
            for line in rec.line_ids:
                acc_id = ""
                if line.account_id.id:
                    acc_id = line.account_id.id
                else:
                    acc_id = rec.journal_id.default_account_id.id
                invoice_line_vals = {
                    "name": line.name,
                    "account_id": acc_id,
                    "quantity": 1.000,
                    "discount": line.discount or 0.00,
                    "price_unit": line.subtotal,
                    "tax_ids": [(6, 0, line.tax_ids.ids)]
                }
                invoice_line.append((0, 0, invoice_line_vals))
            vals.update({"invoice_line_ids": invoice_line})
            # creates invoice
            account_invoice_id = self.env["account.move"].create(vals)
            rec.write({'move_id': account_invoice_id.id})
            account_invoice_id.action_post()
            # if ctx.get("is_paid", False):
            vals = {'journal_id': rec.journal_ids.id,
                    'amount': account_invoice_id.amount_total,
                    'payment_date': account_invoice_id.invoice_date,
                    'communication': account_invoice_id.name,
                    'payment_type': 'inbound',
                    }
            register_payment = self.env['account.payment.register']. \
                with_context(active_id=account_invoice_id.id,
                             active_ids=[account_invoice_id.id],
                             active_model='account.move',
                             dont_redirect_to_payments=True).create(vals)
            register_payment._compute_payment_method_id()
            register_payment.with_context(
                    dont_redirect_to_payments=True).action_create_payments()
            rec.write({'payment_date': register_payment.payment_date})
            invoice_obj = self.env.ref("account.view_move_form")
            return {
                "name": _("Pay Fees"),
                "view_mode": "form",
                "res_model": "account.move",
                "view_id": invoice_obj.id,
                "type": "ir.actions.act_window",
                "target": "current",
                "res_id": account_invoice_id.id,
                "context": {},
            }


class StudentPayslipLineLine(models.Model):
    """Function Line."""

    _name = "student.payslip.line.line"
    _description = "Function Line"
    _order = "sequence"

    slipline_id = fields.Many2one(
            "student.payslip.line", "Slip Line Ref", help="Student payslip line"
    )
    slipline1_id = fields.Many2one(
            "student.fees.structure.line", "Slip Line", help="Student payslip line"
    )
    sequence = fields.Integer(help="Sequence of payslip")
    academic_year_id = fields.Many2one(
            "academic.year", "Academic Year", help="Academic starting Year"
    )
    from_month = fields.Many2one("academic.month", help="Academic starting month")
    to_month = fields.Many2one("academic.month", help="Academic end month")

    @api.constrains("academic_year_id", "from_month", "to_month")
    def check_month(self):
        """Constraint on month"""
        for rec in self:
            if (
                    rec.from_month.date_start
                    and rec.to_month.date_stop
                    and rec.to_month.date_stop < rec.from_month.date_start
            ):
                raise ValidationError(_("To Month should be greater than From Month!"))
            if (
                    rec.academic_year_id
                    and rec.from_month.date_start
                    and rec.to_month.date_stop
            ):
                line_ids = self.search(
                        [
                            ("slipline1_id", "=", rec.slipline1_id.id),
                            ("id", "!=", rec.id),
                            ("academic_year_id", "=", rec.academic_year_id.id),
                            ("from_month", "!=", False),
                            ("to_month", "!=", False),
                        ]
                )
                for old_month in line_ids:
                    if (
                            old_month.from_month.date_start
                            <= rec.from_month.date_start
                            <= old_month.to_month.date_stop
                            or old_month.from_month.date_start
                            <= rec.to_month.date_stop
                            <= old_month.to_month.date_stop
                    ):
                        raise ValidationError(
                                _("Error! You cannot define overlapping months!")
                        )


class AccountMove(models.Model):
    _inherit = "account.move"

    student_payslip_id = fields.Many2one(
            "student.payslip",
            string="Student Payslip",
            help="Select student payslip",
    )


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        """
        Override method to write paid amount in hostel student
        """
        res = super(AccountPaymentRegister, self).action_create_payments()
        invoice = False
        curr_date = fields.Date.today()
        for rec in self:
            if self._context.get("active_model") == "account.move":
                invoice = self.env["account.move"].browse(
                        self._context.get("active_ids", [])
                )
            vals = {}
            #        'invoice_ids' deprecated field instead of this
            #                             used delegation with account_move
            vals.update({"due_amount": invoice.amount_residual})
            if invoice.student_payslip_id and invoice.payment_state == "paid":
                # Calculate paid amount and changes state to paid
                fees_payment = invoice.student_payslip_id.paid_amount + rec.amount
                vals.update(
                        {
                            "state": "paid",
                            "payment_date": curr_date,
                            "move_id": invoice.id or False,
                            "paid_amount": fees_payment,
                            "due_amount": invoice.amount_residual,
                        }
                )
            if invoice.student_payslip_id and invoice.payment_state == "not_paid":
                # Calculate paid amount and due amount and changes state
                # to pending
                fees_payment = invoice.student_payslip_id.paid_amount + rec.amount
                vals.update(
                        {
                            "state": "pending",
                            "due_amount": invoice.amount_residual,
                            "paid_amount": fees_payment,
                        }
                )
            invoice.student_payslip_id.write(vals)
        return res


class StudentFees(models.Model):
    _inherit = "student.student"

    def set_alumni(self):
        """Override method to raise warning when fees payment of student is
        remaining when student set to alumni state"""
        student_payslip_obj = self.env["student.payslip"]
        for rec in self:
            if student_payslip_obj.search(
                    [
                        ("student_id", "=", rec.id),
                        ("state", "in", ["confirm", "pending"]),
                    ]
            ):
                raise ValidationError(
                        _(
                                "You cannot alumni student because payment of fees "
                                "of student is remaining!"
                        )
                )
            return super(StudentFees, self).set_alumni()


class EmsPaymentTypes(models.Model):
    _name = "ems.payment.types"
    _description = "Payment Types for fees structure."

    name = fields.Char("Name")
    description = fields.Text("Description")


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        ctx = self._context or {}
        if 'country' in ctx:
            con = self.env['res.country'].browse(ctx['country'])
            if con.code == "SA":
                args = [('id', '=', False)]
        return super(AccountTax, self)._search(args=args, offset=offset, limit=limit, order=order, count=count,
                                               access_rights_uid=access_rights_uid)


class StudentYearlyFees(models.Model):
    _name = "student.yearly.fees"
    _description = "Configure Yearly and trimesterly fees for students per grade"

    name = fields.Char("Name")
    year = fields.Many2one("academic.year", string="Year")
    school = fields.Many2one("school.school", string="School")
    grade = fields.Many2one("school.standard", string="Grade")
    total = fields.Float("Total Fees", required=True)
    t1 = fields.Float("T1")
    t2 = fields.Float("T2")
    t3 = fields.Float("T3")
    
    @api.onchange('total')
    def calculateterms(self):
        self.t1 = self.total * 0.4
        self.t2 = self.total * 0.3
        self.t3 = self.total * 0.3


class StudentDiscountFees(models.Model):
    _name = "student.discount.fees"

    name = fields.Char("Name")
    discount_amount = fields.Float("Discount Amount")