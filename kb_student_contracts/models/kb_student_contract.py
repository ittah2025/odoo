from odoo import models, api, _, fields

class StudentContract(models.Model):
    _name = 'kb.student.contracts'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_yearInfo'
    _description = 'Student Contract'

    # kb_StudentName = fields.Many2one('student', string="Student Name", tracking=True, readonly=True)
    # kb_yearInfo = fields.Many2one('academic_year', string='Academic Year', help="Related academic year", tracking=True, readonly=True)
    kb_startDate = fields.Date(related='kb_yearInfo.date_start', string='Start Date', required=True, help="Related academic year", tracking=True)
    kb_ednDate = fields.Date(related='kb_yearInfo.date_stop', string='End Date', required=True, help="Related academic year", tracking=True)
    kb_grade = fields.Many2one(related='kb_StudentName.grades', string='Grade', tracking=True)
    # kb_createdBy = fields.Many2one('hr.employee', string='Created By')

    # # print student contract report
    # def print_student_contracts(self):
    #     student_list =[]
    #     data = {
    #         'form_data': self.read()[0],
    #         'student_list_id': student_list
    #     }
    #     tuitionFeesForBoys = self.env['kb.tuition.fees.for.boys'].search([])
    #     tuitionFeesForGirls = self.env['kb.tuition.fees.for.girls'].search([])
    #     for record in self:
    #         for b in tuitionFeesForBoys:
    #             for g in tuitionFeesForGirls:
    #                 value = {

    #                     'kb_createdBy':record.kb_createdBy.name,
    #                     'kb_jobPosition':record.kb_createdBy.job_title,

    #                     'kb_parentName': record.kb_StudentName.Parent_ids.name,
    #                     'kb_parentNationality': record.kb_StudentName.Parent_ids.nationality,
    #                     'kb_parentNationalityID': record.kb_StudentName.Parent_ids.parent_nat_id,
    #                     'kb_parentPhone': record.kb_StudentName.Parent_ids.phone,
    #                     'kb_parentEmail': record.kb_StudentName.Parent_ids.email,

    #                     'kb_StudentName': record.kb_StudentName.name,
    #                     'kb_nationalityID': record.kb_StudentName.student_nat_id,
    #                     'kb_gender': record.kb_StudentName.gender,
    #                     'kb_birthdayDate': record.kb_StudentName.birthdayDate,
    #                     'kb_grade': record.kb_StudentName.grades.name,

    #                     'kb_relativeName': record.kb_StudentName.Parent_ids.otherrelative,
    #                     'kb_othernationality': record.kb_StudentName.Parent_ids.othernationality,
    #                     'kb_otherparent_nat_id': record.kb_StudentName.Parent_ids.otherparent_nat_id,
    #                     'kb_Othermobile': record.kb_StudentName.Parent_ids.Othermobile,

    #                     'kb_relativeName': record.kb_StudentName.kb_relativeName,
    #                     'kb_relative': record.kb_StudentName.kb_relative,
    #                     'kb_relativeNationality': record.kb_StudentName.kb_relativeNationality,
    #                     'kb_relativeNationalityID': record.kb_StudentName.kb_relativeNationalityID,
    #                     'kb_relativePhone': record.kb_StudentName.kb_relativePhone,
    #                     'kb_legitimateAgency': record.kb_StudentName.kb_legitimateAgency,
    #                     'kb_legitimateAgencyDate': record.kb_StudentName.kb_legitimateAgencyDate,
    #                     'kb_custodyBond': record.kb_StudentName.kb_custodyBond,
    #                     'kb_custodyBondDate': record.kb_StudentName.kb_custodyBondDate,
    #                     'kb_guardianship': record.kb_StudentName.kb_guardianship,
    #                     'kb_guardianshipDate': record.kb_StudentName.kb_guardianshipDate,

    #                     'kb_internationalFees':b.kb_internationalFees,
    #                     'kb_primaryFirstGrade':b.kb_primaryFirstGrade,
    #                     'kb_primarySecondGrade':b.kb_primarySecondGrade,
    #                     'kb_primaryOtherGrade':b.kb_primaryOtherGrade,
    #                     'kb_intermediateFees':b.kb_intermediateFees,
    #                     'kb_secondaryFirstGrade':b.kb_secondaryFirstGrade,
    #                     'kb_secondaryOtherGrade':b.kb_secondaryOtherGrade,

    #                     'kb_internationalFees_g':g.kb_internationalFees_g,
    #                     'kb_primaryFirstGrade_g':g.kb_primaryFirstGrade_g,
    #                     'kb_primarySecondGrade_g':g.kb_primarySecondGrade_g,
    #                     'kb_primaryOtherGrade_g':g.kb_primaryOtherGrade_g,
    #                     'kb_intermediateFees_g':g.kb_intermediateFees_g,
    #                     'kb_secondaryFirstGrade_g':g.kb_secondaryFirstGrade_g,
    #                     'kb_secondaryOtherGrade_g':g.kb_secondaryOtherGrade_g,

    #                 }
    #                 student_list.append(value)
    #         return self.env.ref('kb_student_contracts.student_contracts_report_id').report_action(self, data=data)
