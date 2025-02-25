# -*- coding: utf-8 -*-
from odoo import api, fields, models,_,Command
from datetime import date, datetime
class VenderRegisterPayment(models.Model):
    _name = "kb.vender.register.payment"
    _description = "Vender Register Payment"
    _inherits = {'account.move': 'move_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_CustomerName'

    kb_internalTransfer = fields.Boolean(string='Internal Transfer')
    kb_payment_type = fields.Selection([
        ('outbound','Send'),
        ('inbound','Receive'),
    ],string='Payment Type' , default='outbound')
    kb_CustomerName = fields.Many2one('res.partner', string='Vendor')
    kb_amount = fields.Float(string='Amount')
    kb_date = fields.Date(string='Date', default=fields.Date.context_today)
    kb_memo = fields.Char(string='Memo')
    journal_id = fields.Many2one('account.journal', string='Journal' , domain="[('type', 'in', ('bank','cash'))]")
    kb_companyBankAccount = fields.Many2one('res.partner.bank' , string='Vendor Bank Account')

    kb_paymentId = fields.Char(string='Number', required=True,
                            copy=False, readonly=True, default=lambda self: _('Draft'))
    note = fields.Char()

    kb_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),
        ('reject', 'Reject'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], readonly=True, default="draft", help='Choose the state', string='Status')

    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Journal Entry', required=True, readonly=True, ondelete='cascade',
        check_company=True)

    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id), ('id', '!=', journal_id)]",
        check_company=True,
    )

    def action_confirm_payment(self):
        if self.kb_payment_type == 'outbound':
            # payable
            self.move_id.update({
                'date': self.kb_date,
                'journal_id': self.journal_id,
                'line_ids': [(0, 0, {
                    'partner_id': self.int_payment_ids.kb_CustomerName.id,
                    'name': 'Customer Payment %s, %s , %s' % (self.int_payment_ids.kb_amount, self.int_payment_ids.kb_CustomerName.name, self.kb_date),
                    'debit': 0.00,
                    'credit': self.kb_amount,
                }),
                             (0, 0, {
                                 'account_id': 54,
                                 'partner_id': self.int_payment_ids.kb_CustomerName.id,
                                 'name': 'Customer Payment %s, %s , %s' % (
                                     self.int_payment_ids.kb_amount, self.int_payment_ids.kb_CustomerName.name,
                                     self.kb_date),
                                 'debit': self.kb_amount,
                                 'credit': 0.00,
                             })
                             ]
            })


        for rec in self:
            # payment_approval_template_id = self.env.ref("kb_register_payment.email_template_for_approve_payment")
            if rec.approval_config_id and rec.approval_config_id.payment_approval_line:
                rec.kb_state = 'waiting'
                rec.approval_info_line = False
                lines = rec.approval_config_id.payment_approval_line
                for line in lines:
                    dictt = []
                    dictt.append((0, 0, {
                        'level': line.level,
                        'user_ids': [(6, 0, line.user_ids.ids)],
                        'group_ids': [(6, 0, line.group_ids.ids)],
                    }))
                    rec.update({
                        'approval_info_line': dictt
                    })
                users = lines[0].user_ids
                rec.level = lines[0].level
                if lines[0].approve_by == 'group':
                    rec.group_ids = lines[0].group_ids
                    rec.user_ids = False
                    users = rec.group_ids.users
                elif lines[0].approve_by == 'user':
                    rec.group_ids = False
                    rec.user_ids = lines[0].user_ids
                    users = lines[0].user_ids

                for user in users:
                    self.env['bus.bus']._sendone(user.partner_id, 'sh_notification_info',
                                                 {'title': _('Notitification'),
                                                  'message': 'You have approval notification for payment'
                                                  })
                else:
                    super(VenderRegisterPayment, rec)

    def action_cancel(self):
        self.kb_state = 'cancel'

    def action_draft(self):
        self.kb_state = 'draft'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Contract'
        if vals.get('kb_paymentId', ('New')) == ('New'):
            vals['kb_paymentId'] = self.env['ir.sequence'].next_by_code(
                'PaymentType.seq') or ('New')
        res = super(VenderRegisterPayment, self).create(vals)
        return res

    def button_open_journal_entry(self):
        ''' Redirect the user to this payment journal.
        :return:    An action on account.move.
        '''
        self.ensure_one()
        return {
            'name': _("Journal Entry"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {'create': True},
            'view_mode': 'form',
            'res_id': self.move_id.id,
        }

    payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',readonly=False, store=True, copy=False,
                                             compute='kb_compute_payment_method_line_id',domain="[('id', 'in', available_payment_method_line_ids)]",)
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line',compute='kb_compute_payment_method_line_fields')

    @api.depends('available_payment_method_line_ids')
    def kb_compute_payment_method_line_id(self):
        for pay in self:
            available_payment_method_lines = pay.available_payment_method_line_ids
            # Select the first available one by default.
            if pay.payment_method_line_id in available_payment_method_lines:
                pay.payment_method_line_id = pay.payment_method_line_id
            elif available_payment_method_lines:
                pay.payment_method_line_id = available_payment_method_lines[0]._origin
            else:
                pay.payment_method_line_id = False

    @api.depends('kb_payment_type', 'journal_id')
    def kb_compute_payment_method_line_fields(self):
        for pay in self:
            pay.available_payment_method_line_ids = pay.journal_id._get_available_payment_method_lines(pay.kb_payment_type)
            to_exclude = pay._get_payment_method_codes_to_exclude()
            if to_exclude:
                pay.available_payment_method_line_ids = pay.available_payment_method_line_ids.filtered(
                    lambda x: x.code not in to_exclude)
    def _get_payment_method_codes_to_exclude(self):
        # can be overriden to exclude payment methods based on the payment characteristics
        self.ensure_one()
        return []

############################################################################

    sh_to_reconcile = fields.Many2many('account.move.line', string="Line to reconcile")
    approval_config_id = fields.Many2one(
        'kb.payment.approval.config', string="Payment Approval Level", compute="_compute_approval_level")
    user_ids = fields.Many2many('res.users', string="Users")
    level = fields.Integer(string="Next Approval Level")
    group_ids = fields.Many2many('res.groups', string="Groups")
    approval_info_line = fields.One2many(
        'kb.approval.info', 'sh_payment_idv')
    rejection_date = fields.Datetime(string="Reject Date")
    reject_by = fields.Many2one(
        'res.users', string="Reject By")
    reject_reason = fields.Char(string="Reject Reason")
    is_approval_user = fields.Boolean(
        'Is Approval User', compute="_compute_is_approval_user")

    def action_approve(self):
        info_line = self.approval_info_line.filtered(
            lambda x: x.level == self.level)
        if info_line:
            info_line.status = True
            info_line.approval_date = datetime.now()
            info_line.approved_by = self.env.user

        curr_line_id = self.env['kb.payment.approval.config.line'].search(
            [('payment_approval_config_id', '=', self.approval_config_id.id), ('level', '=', self.level)])
        nxt_line_id = self.env['kb.payment.approval.config.line'].search(
            [('payment_approval_config_id', '=', self.approval_config_id.id), ('id', '>', curr_line_id.id)], limit=1)

        if nxt_line_id:
            self.level = nxt_line_id.level
            # if nxt_line_id.approve_by == 'group':
            #     self.group_ids = nxt_line_id.group_ids
            #     self.user_ids = False
            #     users = self.group_ids.users
            if nxt_line_id.approve_by == 'user':
                self.group_ids = False
                self.user_ids = nxt_line_id.user_ids
                users = nxt_line_id.user_ids

            for user in users:
                self.env['bus.bus']._sendone(user.partner_id, 'sh_notification_info',
                                             {'title': _('Notitification'),
                                              'message': 'You have approval notification for payment'
                                              })
        else:
            if self.user_id:
                self.env['bus.bus']._sendone(self.user_id.partner_id, 'sh_notification_info',
                                             {'title': _('Notitification'),
                                              'message': 'Dear User!! Your payment request has been approved'
                                              })
            self.write({'level': 0,
                        # 'group_ids': False,
                        'user_ids': False})

            self.kb_state = 'posted'

    @api.depends('kb_amount')
    def _compute_approval_level(self):
        for rec in self:
            rec.approval_config_id = False
            rec.approval_config_id = rec.env['kb.payment.approval.config'].search(domain=[(
                'min_amount', '<', rec.kb_amount), ('company_ids.id', 'in', [rec.env.company.id])],
                order='min_amount desc', limit=1)

    def _compute_is_approval_user(self):
        self.is_approval_user = False
        for rec in self:
            if self.env.user in self.user_ids or any(item in self.env.user.groups_id.ids for item in rec.group_ids.ids):
                rec.is_approval_user = True

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ['account.move']

    int_payment_ids = fields.One2many('kb.vender.register.payment', 'move_id', string='Internal payment')

