from odoo import api, fields, models, _

class TuitionFeesForBoys(models.Model):
    _name ='kb.tuition.fees.for.boys'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_yearID'

    # kb_yearID = fields.Many2one('academic_year', 'Academic Year', required=True, help="Related academic year ")

    kb_internationalFees = fields.Char(string='International Section Fees',  track_visibility=True)
    # Primary
    kb_primaryFirstGrade = fields.Char(string='First Grade', track_visibility=True)
    kb_primarySecondGrade = fields.Char(string='Second Grade', track_visibility=True)
    kb_primaryOtherGrade = fields.Char(string='Other Grade', track_visibility=True)
    # Intermediate
    kb_intermediateFees = fields.Char(string='Intermediate Fess', track_visibility=True)
    # secondary
    kb_secondaryFirstGrade = fields.Char(string='First Grade', track_visibility=True)
    kb_secondaryOtherGrade = fields.Char(string='Other Grade', track_visibility=True)