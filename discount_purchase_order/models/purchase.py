# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    
    @api.depends('order_line.price_total', 'order_line.discount_type',
                 'order_line.discount', 'global_order_discount',
                 'global_discount_type')
    def _amount_all(self):
        tax = False
        tax_amounts = 0.0
        for order in self:
            amount_untaxed = amount_tax = total_discount = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                if line.taxes_id:
                    tax = True
                    tax_amounts = (line.taxes_id.amount / 100)
                else:
                    tax = False
                if line.discount_type == 'fixed':
                    total_discount += line.discount
                else:
                    total_discount += line.price_unit * line.product_qty * (
                        (line.discount or 0.0) / 100.0)

            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            
            if discTax == 'taxed':
                total = amount_untaxed + amount_tax
            else:
                total = amount_untaxed
                

            if order.global_discount_type == 'fixed':
                total_global_discount = order.global_order_discount
            else:
                total_global_discount = total * (order.global_order_discount or 0.0) / 100
            total -= total_global_discount
            amount_untaxed = total
            total_discount += total_global_discount
            if tax:
                amount_tax = total * tax_amounts
            else:
                amount_tax = 0
            # raise ValidationError(_("{}\n{}\n{}\n".format(amount_untaxed, amount_tax, total)))
            if discTax != 'taxed':
                total += amount_tax
            # raise UserError(_(amount_tax))
            currency = order.currency_id or order.partner_id.property_purchase_currency_id or self.env.company.currency_id
            
            order.update({
                'amount_untaxed': currency.round(amount_untaxed),
                'amount_tax': currency.round(amount_tax),
                'amount_total': currency.round(total),
                'total_global_discount': currency.round(total_global_discount),
                'total_discount': currency.round(total_discount),
            })
            

    total_global_discount = fields.Monetary(string='Total Global Discount', store=True,
                                            readonly=True, compute='_amount_all')
    total_discount = fields.Monetary(string='Total Discount', store=True, readonly=True,
                                     compute='_amount_all', tracking=True)
    global_discount_type = fields.Selection(
        [('fixed', 'Fixed'), ('percent', 'Percent')],
        string="Discount Type",
        default="percent",
        help="If global discount type 'Fixed' has been applied then no partial invoice will be generated for this order.")
    global_order_discount = fields.Float(string='Global Discount', store=True, tracking=True)

    def _prepare_invoice(self):
        self.ensure_one()
        if self.global_order_discount and not self.env.company.discount_account_bill:
            raise UserError(
                _("Global Discount!\nPlease first set account for global discount in purchase setting."))
        if self.global_order_discount and self.global_discount_type == 'fixed':
            lines = self.order_line.filtered(
                lambda l: l.product_id.purchase_method != 'purchase' and l.product_qty != l.qty_received)
            if lines:
                raise UserError(
                    _("This action is going to make bill invoice for the less quantity recieved of this order.\n It will not be allowed because 'Fixed' type global discount has been applied."))
        vals = super(PurchaseOrder, self)._prepare_invoice()
        vals.update({
            'global_discount_type': self.global_discount_type,
            'global_order_discount': self.global_order_discount,
        })
        return vals

    def action_view_invoice(self, invoices=False):
        moves = super(PurchaseOrder, self).action_view_invoice(invoices)
        _logger.info("=========%r",invoices)
        # invoices._compute_amount() 
        # invoices.with_context({'check_move_validity':False}).action_update_discount()
        return moves


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('price_unit', 'discount_type', 'discount', 'taxes_id', 'product_qty')
    def _get_line_subtotal(self):
        for line in self:
            if line.discount_type == 'fixed':
                price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
                quantity = 1
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                quantity = line.product_uom_qty

            taxes = line.taxes_id.compute_all(price, line.order_id.currency_id, quantity,
                                              product=line.product_id, partner=line.order_id.partner_id)
            _logger.info("========%r",taxes)
            line.line_sub_total = taxes['total_excluded']

    line_sub_total = fields.Monetary(compute='_get_line_subtotal',
                                     string='Line Subtotal', readonly=True, store=True)
    discount = fields.Float(string='Discount', digits='Discount', default=0.0)
    discount_type = fields.Selection(
        [('fixed', 'Fixed'), ('percent', 'Percent')],
        string="Discount Type",
        default="percent")

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount', 'discount_type')
    def _compute_amount(self):
        return super(PurchaseOrderLine, self)._compute_amount()

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.
        :return: A python dictionary.
        """
        self.ensure_one()
        quantity = 1.0
        if self.discount_type == 'fixed':
            price = self.price_unit * self.product_uom_qty - (self.discount or 0.0)
        else:
            price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
            quantity = self.product_uom_qty
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.taxes_id,
            price_unit=price,
            quantity=quantity,
            price_subtotal=self.price_subtotal,
        )


    def _prepare_compute_all_values(self):
        vals = super(PurchaseOrderLine, self)._prepare_compute_all_values()
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        quantity = self.product_qty
        if self.discount_type == 'fixed':
            quantity = 1.0
            price = self.price_unit * self.product_qty - (self.discount or 0.0)
        vals.update({
            'price_unit': price,
            'quantity': quantity,
        })
        return vals

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        res.update({
            'discount_type': self.discount_type,
            'discount': self.discount,
        })
        return res
