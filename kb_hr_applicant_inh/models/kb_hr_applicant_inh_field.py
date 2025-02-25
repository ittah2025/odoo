from odoo import api, fields, models, _


class kb_hr_applicant_new_fileds(models.Model):
    _inherit = 'hr.applicant'

    kb_gender = fields.Selection([('male', 'Male'),
                                  ('female', 'Female'),
                                  ], required=False, help='Gender', string='Gender')
    kb_marital_status = fields.Char('Marital Status')
    kb_age = fields.Integer('Age')
    kb_nationality = fields.Many2one('res.country', 'Nationality (Country)')
    kb_location = fields.Char('Location Of The House')
    kb_qualification = fields.Char('Applicant qualification')
    kb_Specialization = fields.Char('Specialization')
    kb_english_level = fields.Selection([('beginner', 'Beginner'),
                                         ('intermediate', 'Intermediate'), ('advanced', 'Advanced')
                                         ], required=False, help='Your English Level', string='Mastery Of English ')
    kb_experience_year = fields.Integer('Years of Experience')
    kb_graduation_year = fields.Integer('Year of Graduation')
    kb_Currently_Employed = fields.Selection([('yes', 'Yes'),
                                              ('no', 'No'),
                                              ], required=False, string='Are You Currently Employed ')
