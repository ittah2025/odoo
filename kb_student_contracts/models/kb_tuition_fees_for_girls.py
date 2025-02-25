from odoo import api, fields, models, _

class TuitionFeesForGirls(models.Model):
    _name ='kb.tuition.fees.for.girls'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_yearID'

    # kb_yearID = fields.Many2one('academic_year', 'Academic Year', required=True, help="Related academic year ")

    kb_internationalFees_g = fields.Char(string='International Section Fees',  track_visibility=True)
    # Primary
    kb_primaryFirstGrade_g = fields.Char(string='First Grade', track_visibility=True)
    kb_primarySecondGrade_g = fields.Char(string='Second Grade', track_visibility=True)
    kb_primaryOtherGrade_g = fields.Char(string='Other Grade', track_visibility=True)
    # Intermediate
    kb_intermediateFees_g = fields.Char(string='Intermediate Fess', track_visibility=True)
    # secondary
    kb_secondaryFirstGrade_g = fields.Char(string='First Grade', track_visibility=True)
    kb_secondaryOtherGrade_g = fields.Char(string='Other Grade', track_visibility=True)