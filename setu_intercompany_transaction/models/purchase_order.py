from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    intercompany_transfer_id = fields.Many2one("setu.intercompany.transfer","Intercompany Transfer", copy=False, index=True)

    # def action_view_invoice(self):
    #     res = super(PurchaseOrder, self).action_view_invoice()
    #     res['context'].update({'default_intercompany_transfer_id': self.intercompany_transfer_id.id})
    #     return res