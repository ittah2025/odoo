# from odoo import http
# from odoo.http import request
#
# class HrEmployeeController(http.Controller):
#
#     @http.route('/kb_employee_dashboard/generate_hr_leave_report', type='json', auth='user')
#     def generate_hr_leave_report(self):
#         model = request.env['hr.employee']
#         report_action = model.sudo().generate_hr_leave_report()
#         return report_action
