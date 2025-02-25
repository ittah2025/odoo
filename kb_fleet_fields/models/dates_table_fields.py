# from calendar import month
# from email.policy import default
# # from typing_extensions import Required
# from odoo import api, fields, models, _
# from datetime import date
# from datetime import datetime
# import re
# from odoo.exceptions import ValidationError
# import logging
# from datetime import date, datetime
#
# _logger = logging.getLogger(__name__)
#
# #
# # class dates_table_fields(models.Model):
# #     _name = "dates_table_fields"
# #     _table = "dates_table_fields"
# #     _description = "dates_table_fields"
# #
# #     id = fields.Integer(string="ID")
# #     form_title_id = fields.Char(string='Document')
# #     name = fields.Char(string="Name")
# #     # start_date_id = fields.Date(string='Start Date')
# #     #
# #     # end_date_id = fields.Date(string="Expiration Date")
# #
# #     note = fields.Text(string="Description")
# #
# #     # @api.model
# #     # def create(self, vals):
# #     #     if not vals.get('note'):
# #     #         vals['note'] = 'New Document title'
# #     #     if vals.get('form_title_id', 'New') == 'New':
# #     #         vals['form_title_id'] = self.env['ir.sequence'].next_by_code(
# #     #             'dates_table_fields') or 'New'
# #     #     res = super(dates_table_fields, self).create(vals)
# #     #     return res
