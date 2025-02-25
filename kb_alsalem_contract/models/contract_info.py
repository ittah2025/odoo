# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import date


class ContractInfo(models.Model):
    _name = "contract.info"
    _description = "Contract Information"
    _rec_name = 'contractId'


    dateH = fields.Date(string='Date:')
    humanResourceName = fields.Many2one('hr.employee', string="Human Resource Employee")
    employeeName = fields.Many2one('hr.employee',string='Employee Name')

    # humanResourceSignutre = fields.Char(string='Human Resource Signutre')
    # employeeSignutre = fields.Char(string='Employee Signutre')

    contractId= fields.Char(string='Contract No ', required=True,
                            copy=False, readonly=True, default=lambda self: _('New'))
    note = fields.Char()

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Contract'
        if vals.get('contractId', ('New')) == ('New'):
            vals['contractId'] = self.env['ir.sequence'].next_by_code(
                'contract.seq') or ('New')
        res = super(ContractInfo, self).create(vals)
        return res