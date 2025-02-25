from odoo import api, fields, models, _
from logging import getLogger




class goods_transfer_tree(models.Model):
    _name = "goods_transfer_tree"
    _table = "goods_transfer_tree"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Goods Transfer"

    GoodsTransfer_id = fields.Many2one('goods_transfer', string="good")


    @api.onchange('no')
    def _get_line_numbers(self):
       # for order in self:
        lno = 1
        for line in self:
                lno += 1
                line.no = lno

    no = fields.Integer( string='No', readonly=True, default=False)
    reportdiscr_2 = fields.Char('Description', groups='base.group_user')
    qty_1 = fields.Char('Qty', groups='base.group_user')
    price_1 = fields.Char('Price', groups='base.group_user')


    