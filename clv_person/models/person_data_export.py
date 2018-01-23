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


class PersonDataExport(models.Model):
    _description = 'Person Data Export'
    _name = 'clv.person.data_export'
    _inherit = 'clv.object.data_export', 'clv.code.model'

    code = fields.Char(string='Data Export Code', required=False, default='/')
    code_sequence = fields.Char(default='clv.data_export.code')

    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_data_export_rel',
        column1='person_id',
        column2='person_data_export_id',
        string='Persons'
    )
    count_persons = fields.Integer(
        string='Persons',
        compute='_compute_count_persons',
        store=True
    )

    @api.depends('person_field_ids')
    def _compute_count_persons(self):
        for r in self:
            r.count_persons = len(r.person_ids)

    person_field_ids = fields.Many2many(
        comodel_name='ir.model.fields',
        relation='clv_person_fields_rel',
        column1='person_id',
        column2='field_id',
        string='Person Fields',
        domain="[('model','=','clv.person')]"
    )
    count_person_fields = fields.Integer(
        string='Person Fields',
        compute='_compute_count_person_fields',
        store=True
    )

    @api.depends('person_field_ids')
    def _compute_count_person_fields(self):
        for r in self:
            r.count_person_fields = len(r.person_field_ids)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]
