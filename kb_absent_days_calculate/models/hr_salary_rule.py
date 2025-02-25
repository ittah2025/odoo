from odoo import api, fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def init(self):
        res = super().init()
        rule_obj = self.env['hr.salary.rule']
        over_time_rule = rule_obj.search([('code', '=', 'OVT')])
        absent_rule = rule_obj.search([('code', '=', 'ABS')])
        over_time_compute = 'gross = categories.Basic + categories.ALW\nover_time_line = payslip.worked_days_line_ids.filtered(lambda x: x.code == "OVT")\nover_time_hours = over_time_line.number_of_hours if over_time_line else 0\nmonth_hours = payslip.kb_month_last_day * payslip.kb_day_work_hours\nhour_price = gross / month_hours if month_hours > 0 else 0\nresult = over_time_hours * hour_price'
        absent_compute = 'gross = categories.Basic + categories.ALW\nabsent_line = payslip.worked_days_line_ids.filtered(lambda x: x.code == "ABSENT")\nabsent_days=absent_line.number_of_days if absent_line else 0\nday_price = gross / 30\nresult = -absent_days * day_price'
        if not over_time_rule:
            overtime_vals = {
                'name': 'OverTime',
                'category_id': 12,
                'code': 'OVT',
                'sequence': 5,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': over_time_compute,
            }
            rule_obj.create(overtime_vals)
        else:
            over_time_rule.update({
                'amount_python_compute': over_time_compute,
            })

        if not absent_rule:
            absent_vals = {
                'name': 'Absent',
                'category_id': 4,
                'code': 'ABS',
                'sequence': 5,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': absent_compute,
            }
            rule_obj.create(absent_vals)
        else:
            absent_rule.update({
                'amount_python_compute': absent_compute
            })
        print("@@@@@@@@@@@@@@@@@")
        return res
