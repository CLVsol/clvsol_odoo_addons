# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models


class Summary(models.Model):
    _description = 'Summary'
    _name = 'clv.summary'
    _order = 'name'

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.name, record.code)
                 ))
        return result

    name = fields.Char(string='Name', required=True)

    code = fields.Char(string='Summary Code', required=False)

    date_summary = fields.Datetime(
        string='Summary Date', required=False, readonly=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Summary Code must be unique!'
         )
    ]
