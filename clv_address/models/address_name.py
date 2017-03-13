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

from openerp import api, fields, models


class Address(models.Model):
    _inherit = 'clv.address'

    name = fields.Char(
        string="Name", required=True, default=False,
        help='Use "/" to get an automatic new Address Name.'
    )
    suggested_name = fields.Char(
        string="Suggested Name", required=False, store=True,
        compute="_get_suggested_name",
        help='Suggested Name for the Address.'
    )
    automatic_set_name = fields.Boolean(
        string='Automatic Name',
        help="If checked, the Address Name will be set automatically.",
        default=True
    )

    @api.depends('street', 'street2')
    def _get_suggested_name(self):
        for record in self:
            if record.street:
                record.suggested_name = record.street
                if record.street2:
                    record.suggested_name = record.suggested_name + ' - ' + record.street2
            else:
                if not record.suggested_name:
                    if record.code:
                        record.suggested_name = record.code
            if record.automatic_set_name:
                record.name = record.suggested_name

    @api.multi
    def write(self, values):
        ret = super(Address, self).write(values)
        for record in self:
            if record.automatic_set_name:
                if record.name != record.suggested_name:
                    values['name'] = record.suggested_name
                    super(Address, record).write(values)
            else:
                if ('name' in values and values['name'] == '/') or \
                   (record.name == '/'):
                    values['name'] = record.suggested_name
                    super(Address, record).write(values)
        return ret
