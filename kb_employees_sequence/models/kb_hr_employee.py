from odoo import api, fields, models,_

class KbHrEmployee(models.Model):
    _inherit = 'hr.employee'

    kb_barcode = fields.Char(string='Badge ID', required=True,
                              copy=False, readonly=True, default=lambda self: _('New'))
    note = fields.Char()

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Employee'
        if vals.get('kb_barcode', ('New')) == ('New'):
            vals['kb_barcode'] = self.env['ir.sequence'].next_by_code(
                'employee.seq') or ('New')
        res = super(KbHrEmployee, self).create(vals)
        return res