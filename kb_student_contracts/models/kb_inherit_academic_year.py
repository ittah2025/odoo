from odoo import models, api, _, fields
class StudentContract(models.Model):
    _inherit = 'academic_year'

    # onchange academic year
    # @api.onchange('current')
    # def onchange_academic_year(self):
    #     for rec in self:
    #         if rec.current == True:
    #             studentInfo = self.env['student'].search([])
    #             for student in studentInfo:
    #                 vals = {
    #                     'kb_StudentName': student.id,
    #                     'kb_yearInfo': self.ids[0],
    #                     }
    #                 self.env['kb.student.contracts'].create(vals)
