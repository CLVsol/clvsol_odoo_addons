# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AbstractPool(models.AbstractModel):
    _description = 'Abstract Pool'
    _name = 'clv.abstract.pool'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

    code = fields.Char(string='Code', required=False)

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         'Error! The Code must be unique!'),
    ]
