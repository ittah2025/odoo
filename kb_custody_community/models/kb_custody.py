from odoo import _, api, fields, models
from datetime import datetime


class HrCustody(models.Model):
    _name = "custody.details"
    _rec_name = 'kb_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    kb_name = fields.Char(string="Custody ID", readonly=True, required=True, copy=False, default='New', tracking=True)
    kb_employee_id = fields.Many2one('hr.employee')
    kb_asset_id = fields.Many2one('account.asset.asset')
    kb_asset_type_id = fields.Many2one('asset.type')
    kb_reason = fields.Char()
    kb_requested_date = fields.Date(tracking=True)
    kb_return_date = fields.Date(tracking=True)
    kb_company_id = fields.Many2one('res.company', string='Company', readonly=True, required=True,
                                    default=lambda self: self.env.user.company_id)
    kb_state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval', 'Waiting For Approval'), ('approved', 'Approved'),
         ('refused', 'Refused'), ('returned', 'Returned')], string='State',
        default='draft', copy=False, tracking=True)
    kb_note = fields.Text()

    @api.model
    def create(self, vals):
        # make a seq to Custody
        if vals.get('name', 'New') == 'New':
            vals['kb_name'] = self.env['ir.sequence'].next_by_code(
                'seq.custody') or 'New'
        result = super(HrCustody, self).create(vals)
        return result

    def action_confirm(self):
        self.kb_requested_date = datetime.today().date()
        self.kb_state = 'waiting_approval'

    def action_approve(self):
        self.kb_state = 'approved'

    def action_refuse(self):
        self.kb_state = 'refused'

    def action_return(self):
        self.kb_return_date = datetime.today().date()
        self.kb_state = 'returned'
