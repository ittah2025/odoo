from odoo import http, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.http import request


import logging

_logger = logging.getLogger(__name__)


class ParentWithdrawal(http.Controller):
    @http.route("/parent/withdrawal", type="http", auth="public", website=True)
    def get_parent_withdrawal(self, **kw):
        return http.request.render("kb_school_withdrawal.parent_withdrawal_web_form")


    @http.route("/parent/withdrawal_check", type="http", auth="public", website=True)
    def get_parent_withdrawal_check(self, kb_id_w, **kw):
        student_model = request.env["student"].sudo().search([('Parent_ids.parent_nat_id', '=', kb_id_w)])

        st_list = list()
        for student in student_model:
            print(f"student_model  ==> {student.name}")
            st_list.append(student.name)

        vals = {
            "st_list": st_list,
            "student_model": student_model,
        }
        return http.request.render("kb_school_withdrawal.parent_withdrawal_web_form_result",vals)

    @http.route("/parent/successful", type="http", auth="public", website=True)
    def get_successful_withdrawal(self, **kw):
        school_withdrawal = request.env['school_withdrawal']
        val = {
            'student_id': kw.get('student_model',False),
            'withdrawal_reason': kw.get('Reason',False),
            'kb_date': kw.get('dates',False),
            'kb_note': kw.get('description',False),
        }
        school_register_id = school_withdrawal.sudo().create(val)
        school_register_id_name = school_register_id.withdrawalID
        print("school_register_id_name", school_register_id_name)
        vals = {
            "school_register_id": school_register_id_name,
        }
        return http.request.render("kb_school_withdrawal.successful_web_form", vals)
