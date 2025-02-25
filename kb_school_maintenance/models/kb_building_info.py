from odoo import api, fields, tools, models, _


class BuildingInfo(models.Model):
    _name = 'kb.building.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Building Information'
    _rec_name = 'kb_buildingName'

    kb_buildingName = fields.Char(string='Building Name', traking=True)

    kb_building_admin = fields.Many2one('hr.employee', string="Maintenance Responsible")




    def _floors_count(self):
        for each in self:
            floors_ids = self.env['building_rooms'].search([('kb_building', '=', self.kb_buildingName)])
            each.floors_count = len(floors_ids)

    def return_action_to_open_floor(self):
        self.ensure_one()
        domain = [
            ('kb_building', '=', self.kb_buildingName)]
        return {
            'name': _('Floors'),
            'domain': domain,
            'res_model': 'building_rooms',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create
                        </p>'''),
            'limit': 80,
            'context': "{'default_building_rooms': '%s'}" % self.id,
        }

    floors_count = fields.Integer(compute='_floors_count', string='# Floors')

