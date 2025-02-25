from odoo import api, fields, tools, models, _
from datetime import datetime


class PrintMaintenanceReports(models.TransientModel):
    _name = 'maintenance_report'





    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    def print_pdf_report(self):

        orders_ids = self.env['kb.maintenance.form'].search([('kb_orderDate', '>=', self.date_from), ('kb_orderDate', '<=', self.date_to)])

        if orders_ids:
            orders_list = []
            for x in orders_ids:
                vals = {
                    'kb_ordersID': x.kb_ordersID,
                    'kb_createdBy': x.kb_createdBy.name,
                    # 'v_state': dict(x._fields['state'].selection).get(x.state),
                    'kb_completedBy': x.kb_completedBy,
                    'kb_orderDate': x.kb_orderDate,
                    'kb_building': x.kb_building.kb_buildingName,
                    'kb_floor': x.kb_floor,
                    'kb_room': x.kb_room.kb_name,
                    'kb_description': x.kb_maintenanceFormID.kb_description,
                    'kb_maintenanceTypeName': x.kb_maintenanceFormID.kb_maintenanceType.kb_maintenanceTypeName,
                }
                orders_list.append(vals)

            print(orders_list)

            data = {
                'form_data': self.read()[0],
                'orders_list_loop': orders_list,
            }
            return self.env.ref('kb_school_maintenance.maintenance_report_print').report_action(self, data=data)

