# from odoo import models, fields, _
#
# class SaleManagement(models.Model):
#     _name = 'kb.sale.management'
#     _description = 'Sale and Purchase Request'
#
#     name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
#     transaction_date = fields.Date(string='Transaction Date')
#     purchaser = fields.Many2one('res.partner', string='Purchaser')
#     seller = fields.Many2one('res.partner', string='Seller')
#     number_of_shares = fields.Integer(string='Number of Shares Sold')
#     price = fields.Float(string='Selling Price')
#     description = fields.Char(string='Description')
#
#     def _get_report_base_filename(self):
#         return _('Sale Management - %s') % (self.name)
