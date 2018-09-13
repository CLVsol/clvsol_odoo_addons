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


class PersonCategory(models.Model):
    _name = "clv.person.category"
    _inherit = 'clv.person.category', 'clv.abstract.model.log'

    log_model = fields.Char(string='Log Model Name', required=True, default='clv.global_log')

    log_ids = fields.One2many(
        string='Global Logs',
        comodel_name='clv.global_log',
        compute='_compute_log_ids_and_count',
    )
