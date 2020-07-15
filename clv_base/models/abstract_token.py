# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import uuid

from odoo import api, fields, models


def get_token():

    return str(uuid.uuid4())


class AbstractToken(models.AbstractModel):
    _description = 'Abstract Token'
    _name = 'clv.abstract.token'
    # _order = 'token'

    token = fields.Char(
        string='Token',
        index=True,
        required=False,
        default='/',
        help='Use "/" to get an automatic new Token.'
    )

    @api.model
    def create(self, values):
        if 'token' not in values or ('token' in values and values['token'] == '/'):
            token = get_token()
            values['token'] = token
        return super().create(values)

    def write(self, values):
        if 'token' in values and values['token'] == '/':
            token = get_token()
            values['token'] = token
        return super().write(values)

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({'token': '/', })
        return super().copy(default)
