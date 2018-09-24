# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ReferenceableModel(models.Model):
    _name = 'clv.referenceable.model'
    _order = 'priority, name'

    base_model = fields.Char(string='Base Model', required=True)
    name = fields.Char(string='Name', required=True, translate=True)
    model = fields.Char(string='Referenceable Model', required=True)
    priority = fields.Integer(string='Priority', default=10)


class AbstractReference(models.AbstractModel):
    _name = 'clv.abstract.reference'

    @api.model
    def referenceable_models(self):
        return [(ref.model, ref.name) for ref in self.env['clv.referenceable.model'].search([
            ('base_model', '=', self._name),
        ])]

    ref_id = fields.Reference(
        selection='referenceable_models',
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
