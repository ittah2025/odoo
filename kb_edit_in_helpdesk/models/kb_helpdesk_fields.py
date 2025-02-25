from odoo import api, fields, models,_
class KbHelpdesk(models.Model):
    _inherit = 'help.ticket'

    kb_userID = fields.Many2one('res.users', string="User Name", default=lambda self: self.env.user, readonly=True)
    kb_userEmail = fields.Char(related='kb_userID.email')
    kb_userPhone = fields.Char(related='kb_userID.phone')
    kb_jobPosition = fields.Char(related='kb_userID.job_title')
    kb_isSolved = fields.Boolean(string='',  compute="pop_up_screen")
    kb_stateName = fields.Char(String='', store=True)

    def inProgress_fun(self):
        for records in self:
            stage_id = self.env['ticket.stage'].search([('name', '=', ' in progress')])
            records.kb_stateName = stage_id.sequence
            records.write({"stage_id": stage_id})

    def solved_fun(self):
        for records in self:
            stage_id = self.env['ticket.stage'].search([('name', '=', 'solved')])
            records.kb_stateName = stage_id.sequence
            records.write({"stage_id": stage_id})

    def cancel_fun(self):
        for records in self:
            stage_id = self.env['ticket.stage'].search([('name', '=', 'canceled')])
            records.write({"stage_id": stage_id})

    def closed_fun(self):
        for records in self:
            stage_id = self.env['ticket.stage'].search([('name', '=', 'closed')])
            records.write({"stage_id": stage_id})

    @api.depends('stage_id')
    def pop_up_screen(self):
        for rec in self:
            if rec.stage_id.name == 'solved':
                self.kb_isSolved = True
            else:
                self.kb_isSolved = False

    def action_send_email(self):
        self.env.ref("kb_edit_in_helpdesk.kb_email_template").send_mail(self.id, force_send=True)

class kBTicket_stage(models.Model):
    _inherit = 'ticket.stage'