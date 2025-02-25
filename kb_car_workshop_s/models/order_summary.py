from calendar import month
from email.policy import default
# from typing_extensions import Required
from odoo import api, fields, models, _
from datetime import date
from datetime import datetime
import re
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class order_summary(models.Model):
   _name = "order_summary"
   _table = "order_summary"
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _description = "Orders Summary Information"

   

    # order_ids2 = fields.Many2one('orders', string="Orders")

    #  @api.onchange('no')
    #  def _get_line_numbers(self):
    #    for order in self:
    #            lno = 1
    #    for line in self:
    #           line.no = lno
    #           lno += 1

   
   ServiceType = fields.Selection([
        ('Mech','Mechanical'),
        ('ECE','Electrical'),
        ('BodyW','Body Work'),
        ('PaintW','Paint'),
        ('oil_W','Oils'),
        ('tireServ','Tires'),
        ('Upholstery','Upholstery'),

         ], string= 'Service Type')

   orederRem = fields.Char('Remarks', groups='base.group_user')
   # techPer = fields.Char('Employee (Primary)', groups='base.group_user')
   techPer = fields.Many2many('hr.employee', string="Technicians")

   # techSecondry = fields.Char('Employee (Helper)', groups='base.group_user')
   techTimein = fields.Datetime(string="Work Start Time")
   techTimeout = fields.Datetime(string="Work End Time")
   statOr = fields.Char('Status', groups='base.group_user')

   total_days = fields.Char(string="Total Time")
   # totalWork = techTimein - techTimeout
   #
   # self.time_diff = str(totalWork.days)

   @api.onchange('techTimein', 'techTimeout', 'total_days')
   def calculate_date(self):
       if self.techTimein and self.techTimeout:
           d1 = datetime.strptime(str(self.techTimein), '%Y-%m-%d %H:%M:%S')
           d2 = datetime.strptime(str(self.techTimeout), '%Y-%m-%d %H:%M:%S')
           self.total_days = d2 - d1
           # raise ValidationError(_("{} after the for\n").format(self.d3))

           # self.total_days = d3

   order_summary_ids = fields.Many2one('orders', string="Order Summary ids")


    

    