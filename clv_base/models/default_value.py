# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DefaultValue(models.Model):
    _description = 'Default Value'
    _inherit = 'clv.abstract.reference'
    _name = 'clv.default_value'
    _order = "model, parameter"

    @api.depends('model', 'parameter')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.model, record.parameter)
                 ))
        return result

    model = fields.Char(string='Model Name ', required=True)
    parameter = fields.Char(string='Parameter ', required=True)

    method = fields.Char(
        string='Method',
        required=False
    )

    method_args = fields.Text(
        string='Method Arguments',
        required=False,
        default='{}'
    )

    value = fields.Char(
        string='Value',
        required=False
    )

    enabled = fields.Boolean(string='Enabled', default=True)

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (model, parameter)',
         u'Error! The Name (model, parameter) must be unique!'),
    ]
