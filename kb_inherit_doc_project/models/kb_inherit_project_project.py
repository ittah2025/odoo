from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)


class kb_Project_project(models.Model):
    _inherit = "project.project"


    # @Fatimah00J
    # document_type_porject=fields.Selection([('invoice','Invoice'),('project','Project')],string='')
    def kb_attachment_tree_view_for_project(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        action['domain'] = str([
            '&',
            '&',
            ('res_model', '=', 'project.project'),
            ('res_id', 'in', self.ids),
            ('document_type_porject', '=', 'project'),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action


    def kb_attachment_tree_view_for_invoice(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        action['domain'] = str([
            '&',
            '&',
            ('res_model', '=', 'project.project'),
            ('res_id', 'in', self.ids),
            ('document_type_porject', '=', 'invoice'),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action

    def kb_attachment_tree_views(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        action['domain'] = str([
            '|',
            '&',
            ('document_type_porject', '!=', ['invoice', 'project']),
            '&',
            ('res_model', '=', 'project.project'),
            ('res_id', 'in', self.ids),
            '&',
            ('res_model', '=', 'project.task'),
            ('res_id', 'in', self.task_ids.ids),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action

class kb_ir_attachment(models.Model):
    _inherit = 'ir.attachment'
    # _inherit = ['ir.attachment','mail.activity.mixin']


    # @Fatimah00J
    document_type_porject=fields.Selection([('invoice','Invoice'),('project','Project')],string='Document type',default='project')
