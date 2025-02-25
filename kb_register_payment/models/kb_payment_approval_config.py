from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PaymentApprovalConfig(models.Model):
    _name = 'kb.payment.approval.config'
    _description = 'Payment Approval Configuration'

    name = fields.Char(string="Name")
    min_amount = fields.Float(string="Minimum Amount", required=True)
    company_ids = fields.Many2many(
        'res.company', string="Allowed Companies", default=lambda self: self.env.company)
    payment_approval_line = fields.One2many('kb.payment.approval.config.line', 'payment_approval_config_id',string='Payment approval line')

    @api.constrains('payment_approval_line')
    def approval_line_level(self):
        if self.payment_approval_line:
            levels = self.payment_approval_line.mapped('level')
            if len(levels) != len(set(levels)):
                raise ValidationError('Levels must be different!!!')


class PaymentApprovalConfigLine(models.Model):
    _name = 'kb.payment.approval.config.line'
    _description = 'Dynamic Payment Approaval Configuration Line'

    level = fields.Integer(string="Level", required=True)
    approve_by = fields.Selection(
        [('user', 'User')], string="Approve Process By", default="user", required=True,)
    user_ids = fields.Many2many('res.users', string="Users")
    group_ids = fields.Many2many('res.groups', string="Groups")
    payment_approval_config_id = fields.Many2one('kb.payment.approval.config')
