# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OffInstance(models.Model):
    _description = 'Off Instance'
    _name = 'clv.off.instance'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

    code = fields.Char(string='Off Instance Code', required=False)

    instance_default = fields.Boolean(string='Instance Default', default=False)

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]
