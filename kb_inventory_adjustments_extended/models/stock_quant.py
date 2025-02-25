from odoo import fields, models, _



class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _quant_tasks(self):
        self._merge_quants()