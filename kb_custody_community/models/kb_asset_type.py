from odoo import api, fields, models


class AssetType(models.Model):
    _name = "asset.type"
    _rec_name = 'kb_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    kb_name_seq = fields.Char(string="Asset Type ID", readonly=True, required=True, copy=False, default='New')
    kb_name = fields.Char(string="Name", required=True, )

    @api.model
    def create(self, vals):
        # make a seq to Concrete
        if vals.get('name', 'New') == 'New':
            vals['kb_name_seq'] = self.env['ir.sequence'].next_by_code(
                'seq.asset') or 'New'
        result = super(AssetType, self).create(vals)
        return result
