from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    kb_custody_count = fields.Integer(compute="compute_custody_count")

    def compute_custody_count(self):
        for rec in self:
            rec.kb_custody_count = self.env['custody.details'].search_count([('kb_employee_id', '=', rec.id)])

    def get_custody(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Custody',
            'view_mode': 'tree,form',
            'res_model': 'custody.details',
            'domain': [('kb_employee_id', '=', self.id)],
            'context': "{'create': False}"
        }
