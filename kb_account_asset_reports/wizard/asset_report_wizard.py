from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AssetReportWizard(models.TransientModel):
    _name = 'asset.report.wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(required=True, default=lambda self: fields.Date.context_today(self), string="End Date")
    categ_ids = fields.Many2many('account.asset.category', string="Asset Category")

    def check_date_range(self):
        if self.date_from < self.date_to:
            raise ValidationError(_('End Date should be greater than Start Date.'))

    def print_pdf(self):
        date_from = self.date_from
        date_to = self.date_to
        categ_ids = self.categ_ids if self.categ_ids else self.env['account.asset.category'].search([])
        asset_ids = self.env['account.asset.asset'].search([('date', '<=', date_to), ('date', '>=', date_from)])

        # raise ValidationError(_("{}, \n\n{}".format(asset_ids, categ_ids.ids)))
        lines = []
        for asset in asset_ids:
            lines.append({
                'asset': asset.name,
                'categ_id': asset.category_id.name,
                'date': asset.date,
                'first_depr_date': asset.first_depreciation_manual_date,
                'gross_value': asset.value,
                'residual_value': asset.value_residual,
                'no_of_entries': asset.method_number,
                'on_entry_every': asset.method_period
            })
        datas = {
            'start_date': date_from,
            'end_date': date_to,
            'data': lines
        }
        return self.env.ref('kb_account_asset_reports.action_asset_report_template').report_action(self, data=datas)


    def print_xlsx(self):
        print("xlsx")
