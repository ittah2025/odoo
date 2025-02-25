from odoo import api, fields, tools, models, _


class ApprovalInfo(models.Model):
    _name = 'kb.approval.info'
    _description = "Approval Information"

    level = fields.Integer(string="Approval Level")
    user_ids = fields.Many2many('res.users', string="Users")
    group_ids = fields.Many2many('res.groups', string="Groups")
    status = fields.Boolean(string="Status")
    approval_date = fields.Datetime(string="Approved Date")
    approved_by = fields.Many2one('res.users', string="Approved By")


    sh_payment_id = fields.Many2one('kb.customer.register.payment')

    sh_payment_idv = fields.Many2one('kb.vender.register.payment')