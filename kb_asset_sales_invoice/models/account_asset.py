# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class AccountAssetAsset(models.Model):
	_inherit = "account.asset.asset"

	invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")
	invoice_ids = fields.One2many('account.move', 'account_asset_asset_id', string="Invoices")

	def _compute_invoice_count(self):
		for rec in self:
			rec.invoice_count = len(self.invoice_ids)

	def open_invoice(self):
		views = 'tree,form' if len(self.invoice_ids) > 1 else 'form'
		res_id = self.invoice_ids.id if len(self.invoice_ids) == 1 else False
		return {
			'name': _(f"{self.name}'s invoices"),
			'type': 'ir.actions.act_window',
			'res_model': 'account.move',
			'view_mode': views,
			'res_id': res_id,
			'domain': [('id', 'in', self.invoice_ids.ids)]
		}

	def _prepare_invoice(self):
		"""
		Prepare invoice from asset
		"""
		self.ensure_one()

		return {
			'ref': self.name or '',
			'move_type': 'out_invoice',
			'invoice_date': self.date,
			'currency_id': self.currency_id.id,
			'partner_id': self.invoice_id.partner_id.id or self.partner_id.id,
			'partner_shipping_id': self.invoice_id.partner_id.id,
			'invoice_origin': self.name,
			'invoice_user_id': self.env.user.id,
			'company_id': self.company_id.id,
			'account_asset_asset_id': self.id,
		}

	def sales_invoice_from_asset(self):
		invoice_id = self.env['account.move'].sudo().create(self._prepare_invoice())
		if self.invoice_id:
			for line in self.invoice_id.invoice_line_ids:
				line.copy({
					'move_id': invoice_id.id,
				})
		else:
			if not self.partner_id:
				raise UserError("Please select partner to create invoice.")
			invoice_id.invoice_line_ids = [(0, 0, {
				'display_type': 'product',
				'sequence': 1,
				'name': self.name,
				'product_id': self.env['product.product'].create({
					'name': self.name,
					'type': 'service',
				}).id,
				'product_uom_id': self.env['uom.uom'].search([], limit=1).id,
				'quantity': 1,
				'price_unit': 1,
				'move_id': invoice_id.id,
			})]
