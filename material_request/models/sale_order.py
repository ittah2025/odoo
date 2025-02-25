from odoo import api, fields, models, _




class SaleOrder(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        index='trigram',
        states={'draft': [('readonly', False)]},
        default=lambda self: _('New'),traking = True)
    qo_num = fields.Char()
# Make the seq for SO different than Quotation
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.quotation', sequence_date=seq_date) or _("New")

        return super().create(vals_list)



    def action_confirm(self):
        res = super().action_confirm()
        if self.state == 'sale':
            self.qo_num = self.name
            seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(self.date_order))
            self.name = self.env['ir.sequence'].next_by_code(
                    'sale.order', sequence_date=seq_date)
        return res