  # -*- coding: utf-8 -*-
# from odoo import http


# class KbAbsentDaysCalculate(http.Controller):
#     @http.route('/kb_absent_days_calculate/kb_absent_days_calculate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kb_absent_days_calculate/kb_absent_days_calculate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kb_absent_days_calculate.listing', {
#             'root': '/kb_absent_days_calculate/kb_absent_days_calculate',
#             'objects': http.request.env['kb_absent_days_calculate.kb_absent_days_calculate'].search([]),
#         })

#     @http.route('/kb_absent_days_calculate/kb_absent_days_calculate/objects/<model("kb_absent_days_calculate.kb_absent_days_calculate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kb_absent_days_calculate.object', {
#             'object': obj
#         })
