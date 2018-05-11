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

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ObjectModelExport(models.AbstractModel):
    _inherit = "clv.object.export"
    _name = 'clv.object.model_export'

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        ondelete='restrict',
        # domain="[('model','in',['clv.person','clv.address'])]"
    )
    model_model = fields.Char(
        string='Model',
        related='model_id.model',
        store=False,
        readonly=True
    )

    model_items = fields.Char(
        string='Model Items',
        compute='compute_model_items',
        store=False
    )

    export_type = fields.Selection(
        [('xls', 'XLS'),
         # ('csv', 'CSV'),
         # ('sqlite', 'SQLite'),
         # ], string='Export Type', readonly=False, required=True
         ], string='Export Type', default='xls', readonly=False, required=True
    )

    export_all_items = fields.Boolean(string='Export All Items', default=True)

    export_domain_filter = fields.Text(
        string='Export Domain Filter',
        required=True,
        help="Export Domain Filter",
        default='[]'
    )

    export_dir_path = fields.Char(
        string='Export Directory Path',
        required=True,
        help="Export Directory Path"
    )

    export_file_name = fields.Char(
        string='Export File Name',
        required=True,
        help="Export File Name"
    )

    def _default_export_date_format(self):
        return self.model_export_date_format()
    export_date_format = fields.Char(
        string='Date Format',
        required=True,
        help="Date Format",
        default=_default_export_date_format
    )

    def _default_export_datetime_format(self):
        return self.model_export_datetime_format()
    export_datetime_format = fields.Char(
        string='Date Time Format',
        required=True,
        help="Date Time Format",
        default=_default_export_datetime_format
    )

    export_all_fields = fields.Boolean(string='Export All Fields', default=True)

    @api.depends('model_model')
    def compute_model_items(self):
        return False

    def model_export_dir_path(self, export_type):
        return False

    def model_export_file_name(self, export_type):
        return False

    def model_export_date_format(self):
        return '%Y-%m-%d'

    def model_export_time_format(self):
        return '%H:%M:%S'

    def model_export_datetime_format(self):
        return "%s %s" % (self.model_export_date_format(), self.model_export_time_format())
