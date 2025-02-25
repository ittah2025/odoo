# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from functools import partial

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def remove_global_discount(self):
        if self.order_line:
            self.order_line.write({
                'global_discount_percent': '',
                'global_discount_amount':0
            })
            self.is_global_discount_applied = False
            self.global_order_discount = 0
            self.order_line._compute_amount()

    def action_update_discount(self):
        if self.order_line:
            if not self.global_order_discount:
                self.order_line.write({
                    'global_discount_percent': '',
                    'global_discount_amount':0

                })
                self.is_global_discount_applied = False
            elif self.global_discount_type == 'percent':
                if self.global_order_discount >100 or self.global_order_discount <0:
                    raise ValidationError("Please enter the valid discount")
                self.order_line.write({
                    'global_discount_percent':str(self.global_order_discount/100),
                    'global_discount_amount':0

                })
                self.is_global_discount_applied = True
            else:
                total_amount = 0
                for line in self.order_line:
                    discount_type = ''
                    discount_type = line.discount_type
                    quantity = line.product_uom_qty
                    if discount_type == 'fixed':
                        line_discount_price_unit = line.price_unit * line.product_uom_qty - line.discount
                        quantity = 1.0
                    else:
                        line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
                    total_amount += line_discount_price_unit*quantity
                if total_amount < self.global_order_discount:
                    raise ValidationError("Discount can't be greater than the order amount")
                self.is_global_discount_applied = True
                self.order_line.write({
                    'global_discount_percent': str(self.global_order_discount/total_amount),
                    'global_discount_amount':0
                })
            self.order_line._compute_amount()



    @api.depends('order_line.price_total', 'order_line.discount_type',
                 'order_line.discount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            total_discount = 0.0
            total_global_discount = 0.0

            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                if line.discount_type == 'fixed':
                    total_discount += line.discount
                else:
                    total_discount += line.product_uom_qty * (line.price_unit - line.price_reduce)
                if line.global_discount_amount:
                    total_global_discount += line.global_discount_amount

            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            if not discTax:
                discTax = 'untax'

            total = amount_untaxed
            if discTax == 'taxed':
                total += amount_tax

            total_discount += total_global_discount

            if discTax != 'taxed':
                total += amount_tax

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': total,
                'total_global_discount': total_global_discount,
                'total_discount': total_discount,
            })

    is_global_discount_applied = fields.Boolean(string="Is Global Discount Applied", default=False)
    total_global_discount = fields.Monetary(string='Total Global Discount', store=True,
                                            readonly=True, compute='_amount_all')
    total_discount = fields.Monetary(string='Discount', store=True, readonly=True,
                                     compute='_amount_all', tracking=True)
    global_discount_type = fields.Selection(
        [('fixed', 'Fixed'), ('percent', 'Percent')], string="Discount Type", default="percent",
        help="If global discount type 'Fixed' has been applied then no partial invoice will be generated for this order.")
    global_order_discount = fields.Float(string='Global Discount', store=True, tracking=True)

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)
        moves._compute_amount()
        moves.with_context({'check_move_validity':False}).action_update_discount()
        return moves

    def action_update_prices(self):
        self.remove_global_discount()
        super(SaleOrder, self).action_update_prices()

    def _prepare_invoice(self):
        invoiceVals = super(SaleOrder, self)._prepare_invoice()
        if self.global_order_discount:
            if self.global_discount_type == 'fixed':
                lines = self.order_line.filtered(
                    lambda l: not l.is_downpayment and l.product_uom_qty != l.qty_to_invoice)
                if lines:
                    raise UserError(_("This action is going to make partial invoice for the less quantity delivered of this order. It will not be allowed because 'Fixed' type global discount has been applied."))
            invoiceVals.update({
                'global_discount_type': self.global_discount_type,
                'global_order_discount': self.global_order_discount
            })
        return invoiceVals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    global_discount_percent = fields.Char("Global Discount Percentage")
    global_discount_amount = fields.Float("Global Discount Amount")
    discount = fields.Float(string='Discount', digits='Discount', default=0.0)
    discount_type = fields.Selection([('fixed', 'Fixed'),
                                      ('percent', 'Percent')],
                                     string="Discount Type",
                                     default="percent")

    @api.onchange('discount','discount_type')
    def onchange_line_discount(self):
        for line in self:
            if line.discount_type and line.discount:
                if line.discount_type == 'percent' and line.discount>100:
                    raise ValidationError("Discount can be greater than 100 percent")
                elif line.discount_type == 'fixed' and line.discount > line.price_subtotal:
                    raise ValidationError("Discount can be greater than line subtotal price")

    @api.onchange('product_uom_qty','discount', 'price_unit', 'tax_id')
    def onchange_update_line_discount(self):
        for line in self:
            if line.discount:
                line._compute_amount()
                if line.order_id.is_global_discount_applied:
                    line.order_id.action_update_discount()

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            quantity = 1.0
            if line.discount_type == 'fixed':
                price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                quantity = line.product_uom_qty
            if line.global_discount_percent:
                line.global_discount_amount = price*float(line.global_discount_percent)*quantity
                price = price - price*float(line.global_discount_percent)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, quantity,
                                            product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        discount = self.discount
        if self.discount_type == 'fixed' and self.product_uom_qty:
            discount = (discount * self.qty_to_invoice) / self.product_uom_qty
        res.update({
            'discount_type': self.discount_type,
            'discount': discount,
        })
        return res
