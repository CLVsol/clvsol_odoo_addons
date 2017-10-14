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


class PersonMng(models.Model):
    _inherit = 'clv.person.mng'

    address_name = fields.Char(
        string="Address Name", required=False, default=False,
        help='Use "/" to get an automatic new Address Name.'
    )
    suggested_address_name = fields.Char(
        string="Suggested Address Name", required=False, store=True,
        compute="_get_suggested_address_name",
        help='Suggested Address Name for the Address.'
    )
    automatic_set_address_name = fields.Boolean(
        string='Automatic Address Name',
        help="If checked, the Address Name will be set automatically.",
        default=True
    )

    @api.depends('street', 'street2')
    def _get_suggested_address_name(self):
        for record in self:
            if record.street:
                record.suggested_address_name = record.street
                if record.street2:
                    record.suggested_address_name = record.suggested_address_name + ' - ' + record.street2
            else:
                if not record.suggested_address_name:
                    if record.street:
                        record.suggested_address_name = record.street
            if record.automatic_set_address_name:
                record.address_name = record.suggested_address_name

    @api.multi
    def write(self, values):
        ret = super(PersonMng, self).write(values)
        for record in self:
            if record.automatic_set_address_name:
                if record.address_name != record.suggested_address_name:
                    values['address_name'] = record.suggested_address_name
                    super(PersonMng, record).write(values)
            else:
                if ('address_name' in values and values['address_name'] == '/') or \
                   (record.address_name == '/'):
                    values['address_name'] = record.suggested_address_name
                    super(PersonMng, record).write(values)
        return ret
