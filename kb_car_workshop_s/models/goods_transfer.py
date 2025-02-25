from odoo import api, fields, models, _
from logging import getLogger


class goods_transfer(models.Model):
    _name = "goods_transfer"
    _table = "goods_transfer"
    _inherit = ['mail.thread','mail.activity.mixin']


    # info 
    transferTo = fields.Char('Transfer To', groups='base.group_user')
    recip = fields.Char('Recipient', groups='base.group_user')
    Addrs = fields.Char('Address', groups='base.group_user')
    psite_1 = fields.Char('Site', groups='base.group_user')
    phon_1 = fields.Char('Site', groups='base.group_user')
    mail_E = fields.Char('Email', groups='base.group_user')


    # link 
    goodtr_ids = fields.One2many('goods_transfer_tree','GoodsTransfer_id', string="damegs")


  
