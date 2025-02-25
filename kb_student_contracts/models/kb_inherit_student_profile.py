from odoo import models, api, _, fields
class StudentContract(models.Model):
    _inherit = 'student'

    kb_relativeName = fields.Char(string='Name')
    kb_relative = fields.Char(string='Relative')
    kb_relativeNationality = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non'),
    ], string='Nationality', help='Choose the Parent nationality')
    kb_relativeNationalityID = fields.Char(string='Nationality ID')
    kb_relativePhone = fields.Char(string='Phone')
    kb_legitimateAgency = fields.Char(string='Legitimate agency NO.')
    kb_legitimateAgencyDate = fields.Date(string='Legitimate agency date')
    kb_custodyBond = fields.Char(string='Custody bond NO.')
    kb_custodyBondDate = fields.Date(string='Custody bond date')
    kb_guardianship = fields.Char(string='Guardianship NO.')
    kb_guardianshipDate = fields.Date(string='Guardianship date')

    # # smart button for count contracts:
    # def contracts_count(self):
    #     for each in self:
    #         contracts_view_ids = self.env['kb.student.contracts'].search([('kb_StudentName', '=', self.name)])
    #         each.contracts_view_count = len(contracts_view_ids)

    # # smart button for contracts:
    # def return_action_to_view_contract(self):
    #     self.ensure_one()
    #     domain = [
    #         ('kb_StudentName', '=', self.name)]
    #     return {
    #         'name': _('Contracts'),
    #         'domain': domain,
    #         'res_model': 'kb.student.contracts',
    #         'type': 'ir.actions.act_window',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'view_type': 'form',
    #         'help': _('''<p class="oe_view_nocontent_create">
    #                        Click to Create for New service
    #                     </p>'''),
    #         'limit': 80,
    #         'context': "{'default_apartment_ids': '%s'}" % self.id,
    #     }
    contracts_view_count = fields.Integer(compute='contracts_count', string='# Contract')