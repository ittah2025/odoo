from odoo import api, fields, models,_






class kb_assets(models.Model):
  _inherit ="account.asset.asset"
  _rec_name = "kb_ordersIDP"

  kb_old_assets= fields.Integer("الرقم النظام القديم")
  kb_ordersIDP = fields.Char(string='رقم اﻷصول', required=True,copy=False, readonly=True,index=True, default=lambda self: _('New'))

  # @api.model
  # def create(self, vals):

  #   if vals.get('kb_ordersIDP', ('New')) == ('New'):
  #     vals['kb_ordersIDP'] = self.env['ir.sequence'].next_by_code(
  #       'ordersIDP.seq') or ('New')
  #   res = super(kb_assets, self).create(vals)
  #   return res
  
  
  
  
  @api.model_create_multi
  def create(self, vals_list):
      for vals in vals_list:
          if vals.get('kb_ordersIDP', _('New')) == _('New'):
              vals['kb_ordersIDP'] = self.env['ir.sequence'].next_by_code('ordersIDP.seq') or _('New')
      res = super(kb_assets, self).create(vals_list)
      return res