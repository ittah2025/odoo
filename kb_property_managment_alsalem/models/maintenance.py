from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError

class Maintenance(models.Model):

    _name = "maintenance"
    _description = "Maintenance Details"


    property_unit =  fields.Many2one('apartments', string="Property Unit")
    maintenance_id = fields.Many2one('rooms', string='Room')
    maintenance_line =  fields.One2many('maintenance.fields', 'maintenance_ids',string='Maintenance Details')
    final_total =  fields.Float(string="Total",  readonly= True , compute="_calculat_total_final" )

    # Room name is related to apartment
    @api.onchange('property_unit')
    def onchange_apartment(self):
        for rec in self:  
            return {'domain': {'maintenance_id': [('aprtment_id','=',rec.property_unit.id)]}}

    # calculate final total of Maintenance 
    @api.depends('final_total')
    def _calculat_total_final(self):
        total= 0 
        for t in self.maintenance_line:
            total += t.totalGeneral
        self.final_total = total

class MaintenanceFields(models.Model):

    _name = "maintenance.fields"
    _description = "Maintenance Details"

    maintenance_ids = fields.Many2one('maintenance')
    amount = fields.Float(string='Quantity')
    totalGeneral = fields.Float(string="Total", compute="_calculate_total_maintenance1")
    description_general = fields.Char(string= 'Description')
    total_cost = fields.Float(string='Cost')

    
    doc_attachment_id3 = fields.Many2many('ir.attachment', 'doc_attach_rel4', 'doc_ids', 'attach_id5', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)


    def _calculate_total_maintenance1(self):
        for rec in self:
            if (rec.amount > 0 ):
                rec.totalGeneral = rec.amount * rec.total_cost 
            else: 
                rec.totalGeneral = rec.total_cost
                rec.amount = 1




# inherit the attachment for document
class Attachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel4 = fields.Many2many('document.fields', 'doc_attachment_id3', 'attach_id5', 'doc_ids',
                                      string="Attachment", invisible=1)

 
