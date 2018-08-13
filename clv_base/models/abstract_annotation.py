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

from datetime import *

from odoo import fields, models


class AbstractAnnotation(models.AbstractModel):
    _name = 'clv.abstract.annotation'
    _order = "date_annotation desc"

    name = fields.Char(string='Subject', index=True, required=False)
    author = fields.Many2one(
        comodel_name='res.users', string='Author', required=True, readonly=True,
        default=lambda self: self._uid
    )
    date_annotation = fields.Datetime(
        string="Annotation Date", required=True, readonly=True,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    body = fields.Text(string='Body')

    active = fields.Boolean(string='Active', default=True)
