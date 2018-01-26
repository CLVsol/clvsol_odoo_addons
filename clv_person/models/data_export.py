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


class DataExport(models.Model):
    _name = 'clv.data_export'
    _inherit = 'clv.data_export'

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        ondelete='restrict',
        # domain="[('model','in',['clv.person'])]"
    )

    data_export_community_id = fields.Many2one(
        comodel_name='clv.community',
        string='Community',
        ondelete='restrict'
    )
    count_data_export_community_persons = fields.Integer(
        string='Community Persons',
        compute='_compute_count_data_export_community_persons',
        store=False
    )

    @api.depends('data_export_community_id')
    def _compute_count_data_export_community_persons(self):
        for r in self:
            r.count_data_export_community_persons = len(r.data_export_community_id.person_ids)

    data_export_person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_data_export_person_rel',
        column1='person_id',
        column2='data_export_id',
        string='Data Export Persons'
    )
    count_data_export_persons = fields.Integer(
        string='Persons',
        compute='_compute_count_data_export_persons',
        store=True
    )

    @api.depends('data_export_person_ids')
    def _compute_count_data_export_persons(self):
        for r in self:
            r.count_data_export_persons = len(r.data_export_person_ids)

    @api.depends('model_model')
    def compute_model_items(self):
        for r in self:
            if self.model_model == 'clv.person':
                r.model_items = 'data_export_person_ids'
        super(DataExport, self).compute_model_items()
