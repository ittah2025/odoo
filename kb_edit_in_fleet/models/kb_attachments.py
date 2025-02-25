# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class kbdocumentattachment(models.Model):
    _name = 'kb_document_attachment'
    _description = "New module for attachment"

    attached_contant = fields.Binary("Attached")
    attach_files = fields.Char('Attached')

    active = fields.Boolean('Active', default=True)

    name= fields.Char('Name', required=True)
    kb_type=fields.Selection([('url','URL'),('file','File')],string='Type')

    kb_url=fields.Char("URL")
    create_uid = fields.Many2one('res.users', string='Created by', index=True, readonly=True)
    write_date = fields.Datetime('Updated on', index=True, readonly=True)
    res_field=fields.Char('Resource Model')
    company_id=fields.Many2one("res.company",'company')

    public=fields.Boolean("Is public document?")
    description=fields.Text('description')


