# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class kb_absent_days_calculate(models.Model):
#     _name = 'kb_absent_days_calculate.kb_absent_days_calculate'
#     _description = 'kb_absent_days_calculate.kb_absent_days_calculate'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
