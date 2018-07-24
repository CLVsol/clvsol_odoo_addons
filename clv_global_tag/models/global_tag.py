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

from odoo import fields, models


class GlobalTag(models.Model):
    _description = 'Global Tag'
    _name = 'clv.global_tag'
    _inherit = 'clv.object.tag'

    code = fields.Char(string='Tag Code', required=False)

    parent_id = fields.Many2one(
        comodel_name='clv.global_tag',
        string='Parent Tag',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='clv.global_tag',
        inverse_name='parent_id',
        string='Child Tags'
    )

    active = fields.Boolean(string='Active', default=True)

    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'Error! The Code must be unique!'),
    ]
