from email.policy import default
# from msilib import sequence
# from typing_extensions import Required
from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError, ValidationError
import re
from odoo.tools.translate import _


class fees_structure(models.Model):
    _name = "fees_structure"
    _table = "fees_structure"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "fees_structure"

    name = fields.Char(string='Name', help='Name of fees structure', required=True, tracking=True)

    code = fields.Char(string='Code', help='Code ', required=True, tracking=True)

    fees_structure_line_ids = fields.One2many('fees_structure_line', 'fees_structure_line_id', string="grade line",
                                              tracking=True)

    @api.model
    def create(self, vals):
        res = super(fees_structure, self).create(vals)
        id_product = self.env['product.template']
        is_analytic_plan = self.env['account.analytic.plan']
        if vals.get('name') == 'Seat reservation fee / رسوم حجز مقعد':
            print('bye')
            product_valu = {
                'name': vals.get('name'),
                'standard_price': 0.0,
                'list_price': 1000,
                'type': 'consu',
                'categ_id': 1,
            }
            analytic_plan_valu = {
                'name': vals.get('name'),
            }
            product_ids = id_product.create(product_valu)
            analytic_plan_ids = is_analytic_plan.create(analytic_plan_valu)
            if product_ids:
                self.write({'id': product_ids.id})
                self.write({'id': analytic_plan_ids.id})
        else:
            print('hi')
            product_valu = {
                'name': vals.get('name'),
                'standard_price': 0.0,
                'list_price': 0.0,
                'type': 'consu',
                'categ_id': 1,
            }
            analytic_plan_valu = {
                'name': vals.get('name'),
            }
            product_ids = id_product.create(product_valu)
            analytic_plan_ids = is_analytic_plan.create(analytic_plan_valu)
            if product_ids:
                self.write({'id': product_ids.id})
                self.write({'id': analytic_plan_ids.id})
        return res


class fees_structure_line(models.Model):
    _name = 'fees_structure_line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'fees_structure_line line'

    sequence = fields.Integer(string="Sequence", required=True, tracking=True)

    name = fields.Char(string="Name", required=True, tracking=True)

    code = fields.Char(string="Code", required=True, tracking=True)

    account = fields.Char(string="Account", required=True, tracking=True)

    taxes = fields.Char(string='Taxes', required=True, tracking=True)

    amount = fields.Char(string="Amount", required=True, tracking=True)

    quantity = fields.Char(string="Quantity", required=True, tracking=True)

    fees_structure_line_id = fields.Many2one('fees_structure', string='grade line', tracking=True)
