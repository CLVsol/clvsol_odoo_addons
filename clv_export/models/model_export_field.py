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


class ModelExportField(models.Model):
    _description = 'Model Export Field'
    _name = "clv.model_export.field"
    _order = "sequence"

    name = fields.Char(string='Alias', index=False, required=False)

    model_export_id = fields.Many2one(
        comodel_name='clv.model_export',
        string='Model Export',
        ondelete='restrict'
    )

    model_id = fields.Many2one(
        string='Model',
        related='model_export_id.model_id',
        store=False
    )

    field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Field',
        ondelete='restrict',
        domain="[('model_id','=',model_id)]"
    )
    field_name = fields.Char(string='Name', related='field_id.name', store=False)
    field_ttype = fields.Selection(string='TType', related='field_id.ttype', store=False)

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    model_export_display = fields.Boolean(string='Display in Export', default=True)


class ModelExport(models.Model):
    _inherit = 'clv.model_export'

    model_export_field_ids = fields.One2many(
        comodel_name='clv.model_export.field',
        inverse_name='model_export_id',
        string='Model Export Fields'
    )

    count_model_export_fields = fields.Integer(
        string='Model Export Fields',
        compute='_compute_count_model_export_fields',
        store=True
    )

    @api.depends('model_export_field_ids')
    def _compute_count_model_export_fields(self):
        for r in self:
            r.count_model_export_fields = len(r.model_export_field_ids)
