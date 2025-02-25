# -*- coding: utf-8 -*-
from email.policy import default
from enum import unique
#from typing_extensions import Required
from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import re
from datetime import date, datetime,timedelta


class student(models.Model):
    _name = "student"
    _table = "student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Information"



    photo = fields.Binary(
        String='photo', help='Choose the student photo for the id card')


    studentID = fields.Char(string='Student ID', required=False,
                            copy=False, readonly=True, default=lambda self: ('New'))

    name = fields.Char(string="Student Full Name En", help="Ener the ",  required=False)
    ar_name = fields.Char(string="Student Name Ar", help = "Enter the  ",  required=False)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=False, help='Choose the student gender')

    transportation = fields.Boolean(string="transportation")
    uniform = fields.Boolean(string="uniform")
    student_id = fields.Boolean(string="ID")


    school_id = fields.Many2one('school', string="School",
                                help='Select school', required=False)


    academic_year = fields.Many2many('academic_year', string="academic_year",
                                help='Select academic_year', required=False)

    fees_id = fields.Many2many('fees', string="fees",
                                help='Select fees', required=False)

    def generat_fees(self):
        for rec in self:
            grade_ids = self.env['fees'].create({
            'student_id'
            })

    course=fields.Char('course')
    grades = fields.Many2one('grade', string="Grade",
                                help='Select Grade', required=False)

    class_id = fields.Many2many('classes', string="classes",
                                help='Select class', required=False)

    academic_year_id = fields.Many2one('academic_year', string="academic year",
                                help='Select academic year', required=False)

    admissionDate = fields.Date(string='Admission Date', required=False, readonly=True)

    phone = fields.Char(string='Student Phone', help='Enter Student Phone', required=False)
    mobile = fields.Char(string='Student Mobile', help='Enter Student Mobile', required=False)
    email = fields.Char(string='Student Email', help='Enter Student Email', required=False)
    nationality = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non'),
    ], help='Choose the student nationality', required=False,string="Nationality")

    note = fields.Text(string="Description", required=False)


    emergencyPhone = fields.Char(
        string='Emergency Phone', help='Enter Emergency Phone', required=False)
    emergencyMobile = fields.Char(
        string='Emergency Mobile', help='Enter Emergency Mobile', required=False)

    Acceptornot = fields.Boolean(string='Accepted', readonly=True )


    ProgramEnrolled= fields.Selection([
        ('diploma','Diploma'),
        ('course','Course'),
        ('both', 'Diploma & Course'),
    ],string='Program Enrolled', required=False)

    educational_level = fields.Selection([
        ('kindergarten','Kindergarten'),
        ('primary','Primary'),
        ('secondary','Secondary'),
        ('intermediate','Intermediate'),
    ], string="Educational Level", required=False)

    the_level = fields.Selection([
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
    ], string='The level')

    student_nat_id = fields.Char(string="National ID", copy=False,  required=False, size=10, unique=True)

    Parent_ids = fields.Many2many('parent', string="Parents", required=False)

    siblings = fields.Integer(compute="siblings_number")
    @api.onchange("student_id")
    def siblings_number(self):
        self.siblings = self.Parent_ids.childs - 1
        if (self.siblings < 0):
            self.siblings = 0
        else:
            self.siblings = self.siblings
    # document_ids = fields.Many2many('document', string="document")
    document_line_ids = fields.One2many('student_document_line_student', 'student_id', string="Document Lines", required=False)
    file = fields.Many2many('ir.attachment', string="Files", required=False)

    # Mail Reminder:
    def mail_reminder(self):
        data =self.env['student_document_line'].search([('name','=',self.student_id.name)])
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            for rec in data:
                if rec.exp_date:
                    id_expiry_date = rec.exp_date - timedelta(days=10)
                    if date_now >= id_expiry_date:
                        mail_content = "  Hello  " + i.name + ",<br>Your Document " + rec.document_types.name + "is going to expire on " + \
                                       str(rec.id_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': ('ID-%s Expired On %s') % (
                            rec.document_types.name, rec.id_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': rec.email,
                    }
                    self.env['mail.mail'].create(main_content).send()


    country_id = fields.Many2one('res.country', string='Country', required=False)
    state_id = fields.Many2one('res.country.state', string='State', required=False)
    street = fields.Char (string="Street", required=False)
    district = fields.Char (string="District", required=False)
    building_number = fields.Char (string="Building Number", required=False)
    city = fields.Char(string="City", required=False)
    postal_code = fields.Char(string="Postal Code", required=False)
    extra_number = fields.Char(string="Extra Number", required=False)

    contract_text = fields.Text(string="Terms Of The Contract", translate=True)


    #previous school page


    previous_school_ids = fields.One2many('previous_school', 'previous_school_id', string="previous school")

    #end of previous school page

    #Medical page

    designation = fields.Char(string='Designation' , help="Enter doctoer designation", required=False)
    doctor_phone = fields.Char(string="Mobile Phone", help="Enter doctor phone", required=False)
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ], string='Blood Group', required=False)
    height = fields.Float(string='Height', help="Hieght in Centimeter",required=False)
    weight = fields.Float(string='Weight', help="Weight in kilogram")
    eye = fields.Boolean(string='Eyes', help='Eye for medical info')
    ear = fields.Boolean(string='Ears', help='Eye for medical info')
    nose_throat = fields.Boolean(string='Nose & Throat',
        help='Nose & Throat for medical info')
    respiratory = fields.Boolean(string='Respiratory',
        help='Respiratory for medical info')
    cardiovascular = fields.Boolean(string='Cardiovascular',
        help='Cardiovascular for medical info')
    neurological = fields.Boolean(string='Neurological',
        help='Neurological for medical info')
    muskoskeletal = fields.Boolean(string='Musculoskeletal',
        help='Musculoskeletal for medical info')
    dermatological = fields.Boolean(string='Dermatological',
        help='Dermatological for medical info')
    blood_pressure = fields.Boolean(string='Blood Pressure',
        help='Blood pressure for medical info')

    #End of Medical page

    #Remark page

    remark_ids = fields.One2many('remark', 'remark_id', string="previous school")


    #end of Remark page

    #grade

    grade_id = fields.Many2many('grade_line', string="classes",
                                help='Select class')

    #end of grade

    # New filed
    medical_diagnosis = fields.Char(string='Medical Diagnosis', required=False)
    address = fields.Char(string='Address', required=False)
    overview = fields.Text(string='Overview about the student', required=False)
    medical_problems = fields.Text(string='Most common medical problems', required=False)
    reason_enroll = fields.Text(string='The reason for your desire to enroll the student in the center', required=False)
    self_care = fields.Text(string='About the level of self-care', required=False)
    behav_prob = fields.Text(string='Most common behavioral problems', required=False)
    source_name = fields.Char(string='Information source name', required=False)
    relationships = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('uncle', 'Cancel'),
        ('cousin', 'Cousin'),
        ('other', 'Other'),
    ], string='Relationship with the student', required=False)


    age = fields.Char("Age", compute='_onchange_age', required=False)
    birthdayDate = fields.Date('Birthday Date', required=False)

    school_min_age = fields.Char(related="school_id.min_age", required=False)
    school_max_age = fields.Char(related="school_id.max_age", required=False)


    # typeofservices = fields.Char(string="The type of services provided")
    # amount_total = fields.Monetary(string="The amount required")
    # trainingtimefrom = fields.Date(string="Training time from")
    # trainingtimeto = fields.Date(string="Training time to")

    Place_of_Birth=fields.Char('Place of Birth')
    passportNo=fields.Char('passportNo')

    Status=fields.Selection([
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
        ], string='Status', required=False)

    sassessment_degree = fields.Many2many('student.assessment.line',string="Transcript", readonly=False,compute="get_class_information")
    subject_id = fields.Many2one(related="sassessment_degree.subject_id")
    graduation_date = fields.Date(required=False)



    def get_class_information(self):
        for rec in self:
            class_info = self.env['student.assessment.line'].search([('student_id', '=', self.name)])
            rec.sassessment_degree = [(5, 0, 0)]
            lines = [(5, 0, 0)]
            for data in class_info:
                # raise ValidationError(_(data.student_assessment_id.subject_id))
                # if not
                if data.final_sem:
                    line_vals = {
                        "student_id": data.student_id.id,
                        "subject_idss": data.subject_idss,
                        'subject':data.student_assessment_id.subject_id.id,
                        # "total_grad": data.total_grad,
                        # "drad_student": data.drad_student,
                        'final_sem': data.final_sem,

                    }
                    lines.append((0, 0, line_vals))

            rec.write({"sassessment_degree": lines})



    @api.onchange('birthdayDate')
    def _onchange_age(self):
        self.age = False
        if self.birthdayDate:
            today = date.today()
            one_or_zero = ((today.month, today.day) < (
                self.birthdayDate.month, self.birthdayDate.day))
            year_difference = today.year - self.birthdayDate.year
            ages = year_difference - one_or_zero
            self.age = ages
            today = date.today()
            school_minAge = int(today.year - int(self.school_min_age))
            school_maxAge = int(today.year - int(self.school_max_age))



    registrsemester=fields.Selection([('first-trimester', 'First Trimester'),
                                  ('second-trimester','Second Trimester'),
                                  ('third-trimester', 'third Trimester')], default='first-trimester',string="Trimester" )

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Student'
        if vals.get('studentID', ('New')) == ('New'):
            vals['studentID'] = self.env['ir.sequence'].next_by_code(
                'student') or ('New')
        res = super(student, self).create(vals)
        return res

    C = fields.Char('base.main_company', required=False)
    fees_num=fields.Char(string="Fees Count", compute="compute_fees")

    def compute_fees(self):
        for rec in self:
            fee=self.env["fees"].search_count([('student_ID', '=', self.studentID)])
            rec.fees_num = fee

    def action_open_fees(self):
            domain = [
                ('student_ID', '=', self.studentID)]
            return {
                'name': _('Fees'),
                'domain': domain,
                'res_model': 'fees',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'target': 'current'
            }
    #
    # assisment_num=fields.Char(string="Assignment Count", compute="compute_assisment")
    # def compute_assisment(self):
    #     for rec in self:
    #         fee=self.env["student_assignment"].search_count([('student_id', '=', self.name)])
    #         rec.assisment_num = fee
    #
    # def action_open_assisment(self):
    #         domain = [
    #             ('student_id', '=', self.name)]
    #         return {
    #             'name': _('Student Assignment'),
    #             'domain': domain,
    #             'res_model': 'student_assignment',
    #             'type': 'ir.actions.act_window',
    #             'view_mode': 'tree,form',
    #             'view_type': 'form',
    #             'target': 'current'
    #         }
    #
    # evaluation_num = fields.Char(string="Evaluation Count", compute="compute_evaluation")
    #
    # def compute_evaluation(self):
    #     for rec in self:
    #         evaluation = self.env["evaluation"].search_count([('student_id', '=', self.name)])
    #         rec.evaluation_num = evaluation
    #
    # def action_open_evaluation(self):
    #     domain = [
    #         ('student_id', '=', self.name)]
    #     return {
    #         'name': _('Student Evaluation'),
    #         'domain': domain,
    #         'res_model': 'evaluation',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'tree,form',
    #         'view_type': 'form',
    #         'target': 'current'
    #     }

    def action_paid(self):
        company = self.school_id.company_id.id
        if (company == ""):

            self.state = 'paid'

            vals = {
                'name': self.name,
                'login':self.name,
                'email': self.email,
                'partner_id':self.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
            }
            users = self.env['res.users'].create(vals)
            return users
        else:
             self.state = 'paid'
             vals = {
                'company_id': company,
                'name': self.name,
                'login':self.name,
                'email': self.email,
                'partner_id':self.id,
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
            }
             users = self.env['res.users'].create(vals)
             return users

    @api.constrains('student_nat_id')
    def _check_National_ID(self):
       
        new_student_nat_id = self.student_nat_id
        
        for old_id in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_id.student_nat_id == self.student_nat_id ):
                raise ValidationError(_(
                    "Error! You cannot define same ID."))


    active= fields.Boolean(string= "Active",default=True)
    Earned_Hr=fields.Float(string="Earned Hours")


    compute_field = fields.Boolean(string="check field", compute='get_user')

    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('kb_Tahtheeb_school.group_school_student'):
            self.compute_field = True
        else:
            self.compute_field = False

    kb_student_line_ids = fields.One2many('student_line', 'kb_student_line_id','Marks')

    kb_total_marks_for_student = fields.Float(compute='get_total_marks_for_student')
    kb_total_hours_for_student = fields.Float(compute='get_total_hours_for_student')

    @api.depends('kb_student_line_ids.kb_total_marks')
    def get_total_marks_for_student(self):

        for line in self:
            line.kb_total_marks_for_student = sum(
                line.kb_student_line_ids.mapped('kb_total_marks')
            )

    @api.depends('kb_student_line_ids.kb_total_hours')
    def get_total_hours_for_student(self):
        for line in self:
            line.kb_total_hours_for_student = sum(line.kb_student_line_ids.mapped('kb_total_hours'))

    kb_gpa_hours_id = fields.Many2one('hours')
    kb_gpa_total_hours = fields.Float(compute='get_kb_total_hours',string="Total Hours")
    kb_gpa_total_points = fields.Float(compute='get_kb_gpa_total_points',string="Total Point")
    kb_total_gpa = fields.Float(compute='get_kb_total_gpa',string="GPA")

    @api.depends('kb_gpa_total_hours', 'kb_gpa_total_points')
    def get_kb_total_gpa(self):
        for rec in self:
            if rec.kb_gpa_total_points and rec.kb_gpa_total_hours:
                rec.kb_total_gpa = rec.kb_gpa_total_points / rec.kb_gpa_total_hours
            else:
                rec.kb_total_gpa = 0

    @api.depends('kb_student_line_ids.kb_points')
    def get_kb_gpa_total_points(self):
        for rec in self:
            total_points = 0.0
            for line in rec.kb_student_line_ids:
                total_points += line.kb_points
            rec.kb_gpa_total_points = total_points

    @api.depends('kb_student_line_ids.kb_total_hours_3')
    def get_kb_total_hours(self):
        for rec in self:
            total_hours = 0.0
            for line in rec.kb_student_line_ids:
                total_hours += line.kb_total_hours_3
            rec.kb_gpa_total_hours = total_hours





class StudentLine(models.Model):
    _name = "student_line"

    kb_student_line_id = fields.Many2one('student',string=' ')
    kb_student = fields.Char('Student')
    kb_class_id = fields.Char('Class')
    kb_subject = fields.Char('Subject')
    year_id=fields.Char('Academic year')
    kb_grade = fields.Char('Grade',compute='get_kb_grade')
    kb_semester = fields.Selection([('mid-semester', 'Mid Semester'), ('final-semester', 'Final Semester')])
    kb_total_marks_2 = fields.Float('Internal')
    kb_total_marks_sum = fields.Float(compute='get_kb_total_marks_sum',string='Internal')
    kb_total_hours_sum = fields.Float(compute='get_kb_total_hours_sum')
    kb_mid_sem = fields.Float('Midterm Mark')
    kb_final_sem = fields.Float('Final Mark')
    kb_total_marks_3 = fields.Float(compute='get_total_marks_3',string='Total Marks')
    kb_total_hours_3 = fields.Float(string='Total Hours')
    kb_trimester = fields.Selection([('first-trimester', 'First Trimester'),
                                     ('second-trimester','Second Trimester'),
                                     ('third-trimester', 'third Trimester')], string="Trimester")
    kb_points = fields.Float(compute='get_kb_points', string="Point")

    kb_mid_sem_2 = fields.Float()
    kb_total_hours = fields.Float()
    kb_total_marks = fields.Float()
    kb_total_hours_2 = fields.Float()

    kb_total_cw_from_mid = fields.Float('Total CW (Midterm)')
    kb_total_hw_from_mid = fields.Float('Total HW (Midterm)')
    kb_cp_from_mid = fields.Float('Total CP (Midterm)')
    totoal_befor_mid=fields.Float(compute='get_totoal_befor_mid')
    kb_total_cw_fin = fields.Float('Total CW (Final)')
    kb_total_hw_fin = fields.Float('Total HW (Final)')
    kb_cp_fin = fields.Float('Total CP (Final)')
    totoal_after_mid=fields.Float(compute='get_totoal_after_mid')

    @api.depends('kb_total_cw_from_mid', 'kb_total_hw_from_mid' ,'kb_cp_from_mid')
    def get_totoal_befor_mid(self):
        for rec in self:
            if rec.kb_total_cw_from_mid and rec.kb_total_hw_from_mid and rec.kb_cp_from_mid:
                rec.totoal_befor_mid = rec.kb_total_cw_from_mid + rec.kb_total_hw_from_mid + rec.kb_cp_from_mid
            else:
                rec.totoal_befor_mid = 0

    @api.depends('kb_total_cw_fin', 'kb_total_hw_fin','kb_cp_fin')
    def get_totoal_after_mid(self):
        for rec in self:
            if rec.kb_total_hw_fin and rec.kb_total_cw_fin and rec.kb_cp_fin:
                rec.totoal_after_mid = rec.kb_total_hw_fin + rec.kb_total_cw_fin+ rec.kb_cp_fin
            else:
                rec.totoal_after_mid = 0



    @api.depends('kb_total_marks_3', 'kb_grade')
    def get_kb_points(self):
        for rec in self:
            if rec.kb_grade == "A":
                rec.kb_points = (rec.kb_total_hours_3 * 5)
            elif rec.kb_grade == "B":
                rec.kb_points = (rec.kb_total_hours_3 * 4.50)
            elif rec.kb_grade == "C":
                rec.kb_points = (rec.kb_total_hours_3 * 4)
            elif rec.kb_grade == "C":
                rec.kb_points = (rec.kb_total_hours_3 * 3.5)
            elif rec.kb_grade == "D":
                rec.kb_points = (rec.kb_total_hours_3 * 3)
            elif rec.kb_grade == "F":
                rec.kb_points = (rec.kb_total_hours_3 * 0)
            else:
                rec.kb_points = 0

    @api.depends('kb_total_marks_3')
    def get_kb_grade(self):
        for rec in self:
            if rec.kb_total_marks_3 >= 90 <= 100:
                rec.kb_grade = "A"
            elif rec.kb_total_marks_3 >= 80 <= 89:
                rec.kb_grade = "B"
            elif rec.kb_total_marks_3 >= 70 <= 79:
                rec.kb_grade = "C"
            elif rec.kb_total_marks_3 >= 60 <= 69:
                rec.kb_grade = "D"
            elif rec.kb_total_marks_3 < 60:
                rec.kb_grade = "F"
            else:
                rec.kb_grade = ''

    @api.depends('kb_total_marks', 'kb_mid_sem', 'kb_total_marks_2', 'kb_mid_sem_2')
    def get_total_marks_3(self):
        for rec in self:
            if rec.kb_total_marks and rec.kb_mid_sem and rec.kb_mid_sem_2 or rec.kb_total_marks_2:
                rec.kb_total_marks_3 = rec.kb_total_marks + rec.kb_mid_sem + rec.kb_total_marks_2 + rec.kb_mid_sem_2
            elif rec.kb_total_marks and rec.kb_mid_sem:
                rec.kb_total_marks_3 = (rec.kb_total_marks + rec.kb_mid_sem)
            else:
                rec.kb_total_marks_3 = 0

    @api.depends('kb_total_marks', 'kb_total_marks_2')
    def get_kb_total_marks_sum(self):
        for rec in self:
            if rec.kb_total_marks and rec.kb_total_marks_2:
                rec.kb_total_marks_sum = rec.kb_total_marks + rec.kb_total_marks_2
            else:
                rec.kb_total_marks_sum = 0

    @api.depends('kb_total_hours', 'kb_total_hours_2')
    def get_kb_total_hours_sum(self):
        for rec in self:
            if rec.kb_total_hours and rec.kb_total_hours_2:
                rec.kb_total_hours_sum = rec.kb_total_hours + rec.kb_total_hours_2
            else:
                rec.kb_total_hours_sum = 0



class Grades(models.Model):
    _name ='student_garades'
    _table = "student_garades"
    _description = "Student grades"

    grades = fields.Char(string='grades', required=False)


class previous_school(models.Model):

    _name = 'previous_school'
    _description = "Student Previous School"

    
    previous_School = fields.Char(string="Prevous School", required=False)
    regisration_number = fields.Char(string="Registration Number", required=False)
    admission_date = fields.Date(string='Admission Date', required=False)
    exit_date = fields.Date(string="Exit Date", required=False)

    previous_school_id = fields.Many2one('student', string='Previous School')

class remark(models.Model):
    _name = 'remark'
    _description = "Student Remark"

    teacher_id = fields.Many2one('teacher', string="Teacher",
                                help='Select teacher')

    teacher_desceription = fields.Text(string = 'Desceription' ,
                                help=' write a desceription about student', required=False)

    remark_id = fields.Many2one('student', string='Previous School')



