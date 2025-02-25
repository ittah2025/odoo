
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError



class damage_tree(models.Model):
    _name = "damage_tree"
    _table = "damage_tree"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Damage line Information"

    damgggg_id = fields.Many2one('damages_report', string="damege")
    no = fields.Integer( string='No', readonly=True, default=False)
    choseSide = fields.Selection([
        ('Rside','Right'),
        ('Lside','Left'),
        ('FRside','Front'),
        ('Bside','Back'),
         ], string= 'Side')
    
    reportdiscr = fields.Char('Description', groups='base.group_user')
    
    # def __init__(self):
    # lno = fields.Integer( string='cc', readonly=False, default=False)
    # @api.onchange('no')
    # def _get_line_numbers(self):
    #    # for order in self:
    #     # if self.lno <= 0 or not self.lno:
    #     #     self.lno = 1
    #     for line in self:
    #         self.lno += 1
    #         line.no = line.lno
    #         # raise ValidationError(_(line.no))
            

    
    


    