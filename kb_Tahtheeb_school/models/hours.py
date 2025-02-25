from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Hours(models.Model):
    _name = 'hours'

    name = fields.Char()
    kb_first_trimester_gpa_hours = fields.Float(default=1)
    kb_second_trimester_gpa_hours = fields.Float(default=1)

    @api.constrains('kb_second_trimester_gpa_hours', 'kb_first_trimester_gpa_hours')
    def check_kb_second_trimester_gpa_hours(self):
        for record in self:
            if record.kb_second_trimester_gpa_hours == 0:
                raise ValidationError(
                    "kb_second_trimester_gpa_hours must be provided when not equal to 0.")
            if record.kb_first_trimester_gpa_hours == 0:
                raise ValidationError(
                    "kb_first_trimester_gpa_hours must be provided when not equal to 0.")
