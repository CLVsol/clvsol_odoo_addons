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

from odoo import api, fields, models


class DocumentReferenceableModel(models.Model):
    _name = 'clv.document.referenceable.model'
    _order = 'priority, name'

    name = fields.Char(required=True, translate=True)
    model = fields.Char(required=True)
    priority = fields.Integer(default=5)


class Document(models.Model):
    _inherit = 'clv.document'

    @api.model
    def document_referenceable_models(self):
        return [(ref.model, ref.name) for ref in self.env['clv.document.referenceable.model'].search([])]

    ref_id = fields.Reference(
        selection='document_referenceable_models',
        string='Refers to')
    ref_model = fields.Char(
        string='Refers to (Model)',
        compute='_compute_reference_model_and_name',
        store=True
    )
    ref_name = fields.Char(
        string='Refers to (Name)',
        compute='_compute_reference_model_and_name',
        store=True
    )

    @api.depends('ref_id')
    def _compute_reference_model_and_name(self):
        for record in self:
            if record.ref_id:
                record.ref_model = record.ref_id._description
                record.ref_name = record.ref_id.name
