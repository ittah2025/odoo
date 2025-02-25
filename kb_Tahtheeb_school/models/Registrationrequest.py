from odoo import api, fields, models
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
from odoo import _


class Registrationrequest(models.Model):
    _name = "registrationrequest"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "registration request"
    _rec_name = "fullstudentname"

    Firstname = fields.Char(string="First Name")
    Fathername = fields.Char(string="Father Name")
    Grandfathername = fields.Char(string="Name")
    Familyname = fields.Char(string="Family Name")
    fullstudentname = fields.Char(string="Full Name")
    phone = fields.Char(string=' Mobile Number')
    email = fields.Char(string=' Email')
    NID = fields.Char(string="National ID/ Iqama")
    Nationality = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non Saudi'),
    ], string='Nationality')

    # Gender= fields.Selection([
    #     ('female', 'Female'),
    #     ('male', 'Male'),
    # ], string='Gender')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('academic_accept', 'Academic Accept'), ('academic_send', 'Send Message'),
        ('managerial_accept', 'Managerial Accept'),
        ('reject', 'Reject'),
    ], string='Status', copy=False, group_expand='_expand_states_here',
        tracking=True, help='Status of the assignment', default='draft', readonly=True)

    birthdayDate = fields.Date('Birthday Date', required=False)
    school_transportation = fields.Selection([
        ('yes_like', 'Yes'),
        ('no_like', 'No'),
    ], string='School transportation')

    Educational_system = fields.Selection([
        ('Private', 'Private'),
        ('international', 'International'),
        ('bi_directional', 'bi-directional'),
    ], string='Educational system')

    country_id = fields.Many2one('res.country', string='Country', required=False)
    company_id = fields.Many2one('res.company', string='Company', required=False)
    city = fields.Char(string="City", required=False)
    street = fields.Char(string="Street", required=False)
    Postal = fields.Char(string="Postal code", required=False)
    Additional = fields.Char(string="Additional code", required=False)

    attachment = fields.Char(string="Attachment", required=False)

    # Father information
    firstnamefather = fields.Char(string="First Name")
    fathernamefather = fields.Char(string="Father Name")
    grandfathernamefather = fields.Char(string="Grandfather Name")
    familynamefather = fields.Char(string="Family Name")
    fullfathername = fields.Char(string="Full Name")
    emailFather = fields.Char(string=' Email')
    phoneFather = fields.Char(string=' Mobile Number')

    NIDfather = fields.Char(string="National ID/ Iqama")

    NationalityFather = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non Saudi'),
    ], string='Nationality')

    attachments = fields.Many2many('ir.attachment', string="Images")
    # Mother Information
    firstnamemother = fields.Char(string="First Name")
    fathernamemother = fields.Char(string="Father Name")
    grandfathernamemother = fields.Char(string="Grandfather Name")
    familynamemother = fields.Char(string="Family Name")
    fullmothername = fields.Char(string="Full Name")
    emailmother = fields.Char(string=' Email')
    phonemother = fields.Char(string=' Mobile Number')

    NIDmother = fields.Char(string="National ID/ Iqama")

    Nationalitymother = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non Saudi'),
    ], string='Nationality')
    # relative Information
    namerelative = fields.Char(string=' Full Name')
    relativerelation = fields.Char(string=' Relative Relation')

    Phonerelative = fields.Char(string="Phone")

    interview_date = fields.Datetime('Interview Date and Time')
    interview_Result = fields.Selection([
        ('pass', 'Pass '),
        ('failed', 'Failed'),
    ], required=False, help='Choose if student pass or failed the interview ', string='Interview Result ')
    interview_note = fields.Char('Interview Note')
    invisibile_butten= fields.Boolean(defult=False)
    def send_massage(self):
        self.state = 'academic_accept'
        if self.interview_date:
            for recoed in self:
                mail_content = "  Dear,  " + str(recoed.name) + \
                               ",<br>  نبارك لك " \
                               "<br>ترشحك لحضور مقابلة تحديد المستوى الدراسي و التي ستكون بتاريخ ." + str(
                    recoed.interview_date) + \
                               ". <br>" \
                               "<br> مع تمنياتنا لكم بالتوفيق"

                template_data = {
                    'subject': _(' المدرسة '),
                    'email_from': self.env.user.partner_id.email,
                    'author_id': self.env.user.partner_id.id,
                    'body': mail_content,
                    'email_to': recoed.email,
                }
                self.env['mail.mail'].create(template_data).send()
                # # Send SMS
                # sms_content = "Dear " + str(
                #     recoed.name) + ", تبارك لك ترشحك للمقابلة الشخصية لتحديد المستوى وذلك بالتفاصيل التالية
                #     ." str(recoed.interview_date) +
                # import requests
                # api_url = ""
                # payload = {
                #     "recipient": recoed.phonerelative,
                #     "message": sms_content
                # }
                # response = requests.post(api_url, data=payload)
                # if response.status_code == 200:
                #     print(f"SMS sent successfully to {recoed.phonerelative}")
                # else:
                #     print(f"Failed to send SMS to {recoed.phonerelative}")

    def interview_reasult(self):
        self.state = 'academic_send'
        print('I am here3')

    def print_action_registrationrequest(self):
        for recoed in self:
            self.state = 'managerial_accept'
            reg_list = []
            student_grp_id = self.env.ref('kb_Tahtheeb_school.group_school_student')
            emp_grp = self.env.ref('base.group_user')
            student_group_ids = [emp_grp.id, student_grp_id.id]
            id_student = self.env['student']
            id_parent = self.env['parent']
            id_user = self.env['res.users']
            # id_contract = self.env['res.partner']
            # if father_is and mother_is:
            valuu = {
                'name': recoed.fullstudentname,
                'student_nat_id': recoed.NID,
                'mobile': recoed.phone,
                'nationality': recoed.Nationality,
                'email': recoed.email,
                # 'gender': recoed.Gender,
                'admissionDate': datetime.now(),
                'birthdayDate': recoed.birthdayDate,
                'city': recoed.city,
                'country_id': recoed.country_id.id,
                'street': recoed.street,
                'building_number': recoed.Postal,
                'postal_code': recoed.Postal,
                'extra_number': recoed.Additional,
                'emergencyPhone': recoed.Phonerelative,
                'emergencyMobile': recoed.Phonerelative,
                # 'emergencyMobile': recoed.Phonerelative,
                # 'Parent_ids': par_ids,
            }

            stu_ids = id_student.create(valuu)
            # user_ids = id_user.create(val)
            # if user_ids:
            #     self.write({'id': user_ids.id})
            if stu_ids:
                # stu_ids.write({'Parent_ids':moth_ids})
                self.write({'id': stu_ids.id})

            father_is = self.env['parent'].search([('parent_nat_id', '=', recoed.NIDfather)])
            mother_is = self.env['parent'].search([('parent_nat_id', '=', recoed.NIDmother)])
            if not mother_is:
                valu = {
                    'name': recoed.fullmothername,
                    'phone': recoed.phonemother,
                    'mobile': recoed.phonemother,
                    'parent_nat_id': recoed.NIDmother,
                    'nationality': recoed.Nationalitymother,
                    'email': recoed.emailmother,
                    'relative': 'mother',
                    'studentID': stu_ids,

                }
                moth_ids = self.env['parent'].create(valu)
                if moth_ids:
                    self.write({'id': moth_ids.id})
            else:
                mother_is.write({'studentID': [(4, stu_ids.id)]})

            if not father_is:
                valu = {
                    'name': recoed.fullfathername,
                    'phone': recoed.phoneFather,
                    'mobile': recoed.phoneFather,
                    'parent_nat_id': recoed.NIDfather,
                    'nationality': recoed.NationalityFather,
                    'email': recoed.emailFather,
                    'relative': 'father',
                    'studentID': stu_ids,

                }
                par_ids = self.env['parent'].create(valu)
                if par_ids:
                    self.write({'id': par_ids.id})
            else:
                father_is.write({'studentID': [(4, stu_ids.id)]})

            # # Send SMS
            # sms_content = "Dear " + str(
            #     recoed.name) + ", تبارك لك ترشحك للقبول وعليك المبادرة بالدخول الى الموقع الالكتروني لاستكمال الاجراءات. سائلين المولى التوفيق والنجاح لكم في مسيرتكم الدراسية."
            # import requests
            # api_url = ""
            # payload = {
            #     "recipient": recoed.phonerelative,
            #     "message": sms_content
            # }
            # response = requests.post(api_url, data=payload)
            # if response.status_code == 200:
            #     print(f"SMS sent successfully to {recoed.phonerelative}")
            # else:
            #     print(f"Failed to send SMS to {recoed.phonerelative}")

    def activity_button_fun(self):
        group_administration = self.env.ref('kb_Tahtheeb_school.group_school_administration').users
        for users in group_administration:
            print(f"userr  ==> {users.id}")
            self.activity_schedule('mail.mail_activity_data_todo', user_id=users.id,
                                   note=f'There is a new Registration Request with name: {self.fullstudentname}')

    def create_invoice_seat(self):
        for recoed in self:
            value = {
                'name': recoed.fullfathername,
                'mobile': recoed.phoneFather,
                'email': recoed.emailFather,
            }

            parent_ids = self.env['res.partner'].create(value)
            if parent_ids:
                tax = self.env['account.tax'].search([('id', '=', 1)])
                product_obj = self.env['product.template'].search(
                    [('name', '=', 'Seat reservation fee / رسوم حجز مقعد')])
                invoice_value = self.env['account.move'].create({
                    'partner_id': parent_ids.id,
                    'invoice_date': date.today(),
                    'move_type': 'out_invoice',
                })
                self.env['account.move.line'].create({
                    'name': product_obj.name,
                    'product_id': product_obj.id,
                    'tax_ids': [(6, 0, tax.ids)],
                    'quantity': 1,
                    'price_unit': product_obj.list_price,
                    'move_id': invoice_value.id,
                })
                if invoice_value:
                    recoed.invisibile_butten =True

