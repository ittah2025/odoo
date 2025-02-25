
import math

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentAssessment(models.Model):
    _name = "studentassessment"
    _description = "Students Assessment based on ClassWork(CW), Class Participation(CP), HomeWork(HW)"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def current_year(self):
        return self.env['academic_year'].search([('current', '=', True)], limit=1)

    name = fields.Char("Name", translate=True,tracking=True,required=False,readonly=True)
    teacher_id = fields.Many2one('teacher', string='Teacher',tracking=True, required=True)
    subject_id = fields.Many2one('subject',string='Subject',tracking=True ,required=True)
    grade_id=fields.Many2one('grade', string='Grade and Section',tracking=True)
    state = fields.Selection([('draft', 'Draft'), 
    ('confirm', 'Confirm'), 
    ('pending', 'Pending'),
    ('done', 'Done'),
    ('locked', 'Locked')], default='draft')
    
    semester = fields.Selection([('mid-semester', 'Mid Trimester'),
                                ('final-semester', 'Final Trimester')], default='mid-semester', required=True)
                                
    trimester = fields.Selection([('first-trimester', 'First Trimester'), ('second-trimester',
                                 'Second Trimester'), ('third-trimester', 'third Trimester')], default='first-trimester', required=True)
    
    no_of_assignments = fields.Integer('No. of Assignments', default=1,tracking=True)

    year_id = fields.Many2one("academic_year", string="Year", tracking=True,default=lambda self: self.current_year())
    exam_month = fields.Many2one("academic_month", string="Exam Month", domain="[('year_id', '=', year_id)]")

    all_marks_entered = fields.Boolean( "All Marks entered", compute="_compute_all_marks")

    assessment_line_ids = fields.One2many('student.assessment.line', inverse_name='student_assessment_id', string='Assesments')

    class_id = fields.Many2one('classes', string='Grade and Section',tracking=True,required=True)

    def _compute_all_marks(self):
        for assess in self:
            if assess.assessment_line_ids and all(assess.assessment_line_ids.mapped('marks_entered_in_line')):
                assess.all_marks_entered = True
            else:
                assess.all_marks_entered = False



    @api.onchange('teacher_id')
    def onchange_apartment(self):
        for rec in self:
            return {'domain': {'subject_id': [('name', '=', rec.teacher_id.subject_id.name)]}}


    @api.onchange("teacher_id")
    def _onchange_teacher_id(self):
        for assessment in self:
            if assessment.teacher_id:
                assessment.subject_id = False
                assessment.class_id = False
    
    def _get_semester_values(self):
        return [val for key, val in type(self).semester.selection if self.semester == key]

    def _get_trimester_values(self):
        return [val for key, val in type(self).trimester.selection if self.trimester == key]

    def name_get(self):
        result = []
        for assessment in self:
            name = assessment.class_id.name_get()[0][1] + ' ' + assessment._get_semester_values()[0]
            result.append((assessment.id, name))
        return result

    @api.model
    def create(self, vals):
        record_exist = self.search(['&',
                                    ('teacher_id', '=', vals['teacher_id']),
                                    '&',
                                    ('subject_id', '=', vals['subject_id']),
                                    '&',
                                    ('class_id', '=', vals['class_id']),
                                    '&',
                                    ('year_id', '=', vals['year_id']),
                                    '&',
                                    ('semester', '=', vals['semester']),

                                    ('trimester', '=', vals['trimester'])])
        if record_exist:
            raise ValidationError(
                _("Assessment already exists with the same Teacher, Subject, Grade and Section, Year,etc"))
        res = super(StudentAssessment, self).create(vals)
        res.name = res.class_id.name_get()[0][1] + ' ' + res._get_semester_values()[0]
        return res

    def action_fetch_students(self):
        for rec in self:
            if self._context.get("done") and rec.state != 'locked':
                # rec.state = 'done'
                return True
            if rec.class_id and not self._context.get("done"):
                # elec = self.env["elective_subject"].search(
                #     [('class_id', '=', rec.class_id.id)]).elective_subject_ids
                # if rec.subject_id.id in elec.ids:
                #     students_rec = self.env["student"].search(
                #         [('class_id', '=', rec.class_id), ('state', 'in', ['done'])]).filtered(
                #         lambda x: rec.subject_id.id in x.elective_subject_ids.ids)
                # else:
                students_rec = self.env["student"].search([('class_id', '=', rec.class_id.id)])
                unlink = [(5, 0, 0)]
                recs = unlink + [(0, 0, {'student_id': student.id,'student_assessment_line_marks_ids':
                    [(0, 0, {'seq': i}) for i in range(rec.no_of_assignments)]}) for student in students_rec]
                rec.assessment_line_ids = recs
                rec.state = 'pending'
        return True

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
        return True

    def mark_done(self):
        for rec in self:
            if rec.all_marks_entered:
                rec.state = 'done'
            else:
                raise ValidationError(_("Marks not Entered Fully"))
        return True

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
        return True

    def lock_marks(self):
        for rec in self:
            rec.state = 'locked'
        return True

    def unlock_marks(self):
        for rec in self:
            rec.state = 'done'
        return True

    def get_client_action(self):
        if self.no_of_assignments < 0:
            raise ValidationError(_("No. of Assignments should not be less than 1"))
        if not self.assessment_line_ids:
            self.action_fetch_students()
        else:
            self.with_context(done=True).action_fetch_students()
        if not self.assessment_line_ids:
            raise ValidationError(
                _("Please add Students for respective Grade"))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "kb_Tahtheeb_school.action_student_assessment_line_marks")
        action['context'] = {'rec': self.id}
        return action

    def get_client_action2(self):
        if not self.assessment_line_ids:
            self.action_fetch_students()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "kb_Tahtheeb_school.action_student_grade_marks")
        action['context'] = {'rec': self.id}
        return action

    @api.model
    def get_students(self, rec):
        students_rec = []
        lines = self.assessment_line_ids.search_read(
            [('student_assessment_id', 'in', rec)])
        for student in lines:
            if student["total_hw"] == -1:
                student["total_hw"] = "N/A"
            if student["total_cw"] == -1:
                student["total_cw"] = "N/A"
            if student["cp"] == -1:
                student["cp"] = "N/A"
            if student["total_marks"] == -1:
                student["total_marks"] = "N/A"
            if student['student_assessment_line_marks_ids']:
                marks = self.env["student.assessment.line.marks"].browse(
                    student['student_assessment_line_marks_ids'])
                if not self._context.get("calculate_total_marks"):
                    student.update(
                        {'cw': [m if m != -1 else 'N/A' for m in marks.mapped('cw')]})
                    student.update({'hw': [m for m in marks.mapped('hw')]})
                student.update(
                    {'assignment_cw': [m for m in marks.mapped('name')]})
                student.update(
                    {'assignment_hw': [m for m in marks.mapped('assignment_hw')]})
        header_details = self.search_read(([('id', 'in', rec)]),
                                          ['name', 'teacher_id', 'class_id', 'subject_id', 'year_id',
                                           'no_of_assignments', 'semester', 'trimester', 'exam_month'])
        return lines, header_details

    @api.model
    def get_student_grade(self, id):
        rec = self.browse(id)
        assessment_rec = self.search(['&',
                                      ('teacher_id', '=', rec.teacher_id.id),
                                      '&',
                                      ('subject_id', '=', rec.subject_id.id),
                                      '&',
                                      ('class_id', '=', rec.class_id.id),
                                      '&',
                                      ('year_id', '=', rec.year_id.id),
                                      '&',
                                      ('semester', '!=', 'tri-sem'), ('trimester', '=', rec.trimester)])

        grades = self.with_context(
            calculate_total_marks=True).get_students(assessment_rec.ids)
        new_student_result = []
        for grade in grades[0]:
            if grade['student_id'] not in [rec['student_id'] for rec in new_student_result]:
                new_student_result.append(grade)
            else:
                if grade['semester'] == 'mid-semester':
                    vals = {
                        "cp2": grade['cp'],
                        "total_hw2": grade['total_hw'],
                        "total_cw2": grade['total_cw'],
                        "total_marks_2": grade['total_marks'],
                        "mid_sem": grade['mid_sem'],
                    }
                elif grade['semester'] == 'final-semester':
                    vals = {
                        "cp2": grade['cp'],
                        "total_hw2": grade['total_hw'],
                        "total_cw2": grade['total_cw'],
                        "total_marks_2": grade['total_marks'],
                        "final_sem": grade['final_sem'],
                    }
                vals.update(vals)
                [rec.update(vals) for rec in new_student_result if rec['class_id'] == grade['class_id']]
        for grade in new_student_result:
            if grade.get('total_marks', False) == 'N/A' or grade.get('total_marks_2', False) == 'N/A':
                grade['total_internal_marks'] = "N/A"
                grade['total_marks_out_100'] = "N/A"
            else:
                grade['total_internal_marks'] = grade['total_marks'] + \
                                                (grade.get('total_marks_2', False) or 0)
                grade['total_marks_out_100'] = grade['total_internal_marks'] + \
                                               grade['mid_sem'] + grade['final_sem']
        return new_student_result, rec._get_trimester_values()[0]

class StudentAssessmentLine(models.Model):
    _name = "student.assessment.line"
    _description = "Students Assessment Line adding HW,CW,CP"
    _rec_name = "student_id"
    _inherit = ['mail.thread']

    student_id = fields.Many2one('student', string='Student',domain='',store=True)
    student_assessment_id = fields.Many2one('studentassessment', string='Student Assessment ID')
    studentID = fields.Many2many('student', string="Students")
    student_assessment_line_marks_ids = fields.One2many('student.assessment.line.marks', inverse_name='student_assessment_line_id', string='Assesments lines')

    total_cw = fields.Float(string="Total CW",help="Total of CW(Class Work)", compute="_compute_cw_hw", tracking=True, store=True)
    total_hw = fields.Float(string="Total HW", help="Total of HW(Home Work)", compute="_compute_cw_hw", tracking=True, store=True)
    cp = fields.Float(string="CP", help="CP(Class Participation)", tracking=True)
    total_marks = fields.Float("Total Marks", compute="_compute_total_marks", tracking=True,
                               help="Total Marks Obtained from CW, HW and CP")
    class_id = fields.Many2one(related="student_assessment_id.class_id")
    semester = fields.Selection(related="student_assessment_id.semester")
    subject_id = fields.Many2one(related="student_assessment_id.subject_id")
    year_id=fields.Many2one(related="student_assessment_id.year_id")
    mid_sem = fields.Float(string='Mid Semester', tracking=True)
    tri_sem = fields.Float(string='Tri Semester', tracking=True)
    final_sem = fields.Float(string='Final Semester', tracking=True)
    subject = fields.Char(string="Subject", compute="assgin_subject")
    subject_idss = fields.Char(string="Subject ID", compute="assgin_subject_id")
    marks_entered_in_line = fields.Boolean(
        "Marks Entered", compute="_compute_marks_entered_in_line")
    kb_boolean_field = fields.Boolean(compute='get_kb_compute',
                                      string='',
                                      required=False)
    kb_related_total_marks = fields.Float(compute='get_kb_related_total_marks')
    kb_related_total_hours = fields.Float(compute='get_kb_related_total_hours')
    kb_related_mid_sem = fields.Float(compute='get_kb_related_mid_sem')

    @api.depends('mid_sem')
    def get_kb_related_mid_sem(self):
        for rec in self:
            if rec.student_assessment_id.semester == 'final-semester':
                rec.kb_related_mid_sem = rec.final_sem
            else:
                rec.kb_related_mid_sem = 0

    @api.depends('total_marks')
    def get_kb_related_total_marks(self):
        for rec in self:
            if rec.student_assessment_id.semester == 'final-semester':
                rec.kb_related_total_marks = rec.total_marks
            else:
                rec.kb_related_total_marks = 0

    @api.depends('total_cw')
    def get_kb_related_total_hours(self):
        for rec in self:
            if rec.student_assessment_id.semester == 'final-semester':
                rec.kb_related_total_hours = rec.total_cw
            else:
                rec.kb_related_total_hours = 0

    @api.depends('total_cw')
    def get_kb_compute(self):
        for rec in self:
            if rec.total_cw > 0:
                rec.kb_boolean_field = True
                vals = {
                    'kb_total_hours': rec.total_cw,
                    'kb_total_marks': rec.total_marks,
                    'kb_student': rec.student_id.studentID,
                    'kb_class_id': rec.student_assessment_id.class_id.class_id,
                    'kb_subject': rec.student_assessment_id.subject_id.name,
                    'year_id': rec.student_assessment_id.year_id.academic_yearID,
                    'kb_semester': rec.student_assessment_id.semester,
                    'kb_mid_sem': rec.mid_sem,
                    'kb_final_sem': rec.final_sem,
                    'kb_total_hours_3': rec.student_assessment_id.subject_id.Hours,
                    'kb_trimester': rec.student_assessment_id.trimester,
                    'kb_total_cw_from_mid':rec.total_cw ,
                    'kb_total_hw_from_mid':rec.total_hw ,
                    'kb_cp_from_mid':rec.cp,
                }
                vals_2 = {
                    'kb_total_marks_2': rec.kb_related_total_marks,
                    'kb_total_hours_2': rec.kb_related_total_hours,
                    'kb_mid_sem_2': rec.kb_related_mid_sem,
                    'kb_final_sem': rec.final_sem,
                    'kb_total_cw_fin': rec.total_cw,
                    'kb_total_hw_fin': rec.total_hw,
                    'kb_cp_fin': rec.cp,
                }
                existing_line = rec.student_id.kb_student_line_ids.filtered(
                    lambda line: line.kb_class_id == vals['kb_class_id'] and line.kb_subject == vals[
                        'kb_subject'] and line.kb_trimester == vals['kb_trimester']
                )
                if existing_line:
                    if vals['kb_semester'] != 'final-semester':
                        existing_line.write(vals)
                    else:
                        existing_line.write(vals_2)  # Append vals_2 to existing line

                else:
                    rec.student_id.kb_student_line_ids = [(0, 0, vals)]
            else:
                rec.kb_boolean_field = False

    @api.depends("total_cw", "total_hw", "cp")
    def assgin_subject(self):
        for rec in self:
            rec.subject = rec.subject_id.name

    @api.depends("total_cw", "total_hw", "cp")
    def assgin_subject_id(self):
        for rec in self:
            rec.subject_idss = rec.subject_id.subject_id


    def _compute_marks_entered_in_line(self):
        for assess_line in self:
            if (-1 not in assess_line.student_assessment_line_marks_ids.mapped('hw')) \
                and (-1 not in assess_line.student_assessment_line_marks_ids.mapped('cw')) \
                    and assess_line.cp != -1 and assess_line.total_marks != -1:
                assess_line.marks_entered_in_line = True
            else:
                assess_line.marks_entered_in_line = False

    @api.depends("total_cw", "total_hw", "cp")
    def _compute_total_marks(self):
        total_marks = 0.00

        def quarter(x):
            return math.ceil(x * 4) / 4

        for rec in self:
            if rec.cp == -1 or rec.total_hw == -1 or rec.total_cw == -1:
                rec.total_marks = -1
            else:
                total_marks = rec.total_cw + rec.total_hw + \
                              (0 if rec.cp == -1 else rec.cp)
                rec.total_marks = quarter(total_marks)

    @api.depends("student_assessment_line_marks_ids.hw", "student_assessment_line_marks_ids.cw")
    def _compute_cw_hw(self):
        total_cw = 0.00
        total_hw = 0.00

        def quarter(x):
            return math.ceil(x * 4) / 4
        for rec in self:
            if rec.student_assessment_line_marks_ids:
                total_cw = sum(
                    rec.student_assessment_line_marks_ids.mapped('cw'))
                total_hw = sum(
                    rec.student_assessment_line_marks_ids.mapped('hw'))
                cw_list = rec.student_assessment_line_marks_ids.mapped('cw')
                if -1 in cw_list:
                    rec.total_cw = -1
                else:
                    rec.total_cw = quarter((
                            total_cw / len(cw_list)))

                hw_list = rec.student_assessment_line_marks_ids.mapped('hw')
                if -1 in hw_list:
                    rec.total_hw = -1
                else:
                    rec.total_hw = quarter((
                            total_hw / len(hw_list)))
            else:
                rec.total_cw = total_cw
                rec.total_hw = total_hw


    def action_show_assesments_line(self):
        # view = self.env.ref('exam.student_assessment_line_view_form')
        view = self.env.ref('kb_Tahtheeb_school.student_assessment_line_view_form_default')
        return {
            'name': _('Assessment Line'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'student.assessment.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.id,
            'context': dict(
                self.env.context,
            ),
        }

class StudentAssessmentLineMarks(models.Model):
    _name = "student.assessment.line.marks"
    _description = "marks of the CW,HW,CP"
    _inherit = ['mail.activity.mixin','mail.thread']

    name = fields.Char(string="Name of Assignment(CW)", help="Assignment for CW")
    seq = fields.Integer(string="Sr No.")
    assignment_hw = fields.Char(string="Name of Assignment(HW)", help="Assignment for HW")
    hw = fields.Float(string="HW", default=-1,tracking=True)
    cw = fields.Float(string="CW", default=-1,tracking=True)
    total = fields.Integer(string='Total')
    student_assessment_line_id = fields.Many2one('student.assessment.line', string='Student Assessment Line ID')
    student_id = fields.Many2one(related="student_assessment_line_id.student_id", store=True)

    def action_show_assesments_line_marks(self):
        view = self.env.ref('kb_Tahtheeb_school.student_assessment_line_marks_view_form_default')
        return {
            'name': _('Assessment Line Marks'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'student.assessment.line.marks',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.id,
            'context': dict(
                self.env.context,
            ),
        }