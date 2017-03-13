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

from openerp import fields, models


class AddressAnotation(models.Model):
    _description = 'Address Annotation'
    _name = 'clv.address.annotation'
    _inherit = 'clv.object.annotation', 'clv.code.model'

    code = fields.Char(string='Annotation Code', required=False)
    code_sequence = fields.Char(default='clv.annotation.code')

    address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address',
        ondelete='cascade'
    )

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]


class Address(models.Model):
    _inherit = "clv.address"

    annotation_ids = fields.One2many(
        comodel_name='clv.address.annotation',
        inverse_name='address_id',
        string='Annotations'
    )
