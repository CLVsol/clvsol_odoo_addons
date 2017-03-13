# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import random

from odoo import api, fields, models


def get_random_field():

    random_field = str(random.randrange(1, 2147483647))
    while len(random_field) < 10:
        random_field = '0' + random_field

    return random_field


class RandomModel(models.AbstractModel):
    _name = 'clv.random.model'
    _order = 'random'

    random_field = fields.Char(
        string='Random ID', index=True, required=False, default='/',
        help='Use "/" to get an automatic new Random ID.'
    )

    @api.model
    def create(self, values):
        if 'random_field' not in values or ('random_field' in values and values['random_field'] == '/'):
            random_field = get_random_field()
            values['random_field'] = random_field
        return super(RandomModel, self).create(values)

    @api.multi
    def write(self, values):
        if 'random_field' in values and values['random_field'] == '/':
            random_field = get_random_field()
            values['random_field'] = random_field
        return super(RandomModel, self).write(values)

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default.update({'random_field': '/', })
        return super(RandomModel, self).copy(default)
