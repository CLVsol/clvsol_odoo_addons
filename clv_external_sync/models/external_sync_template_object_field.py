# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ExternalSyncTemplateObjsctField(models.Model):
    _description = 'External Sync Template Object Field'
    _name = "clv.external_sync.template.object_field"
    _order = "sequence"

    external_object_field = fields.Char(string='External Object Field')
    local_object_field = fields.Char(string='Local Object Field')

    inclusion = fields.Boolean(string='Use during Inclusion', default=False)
    update = fields.Boolean(string='Use during Update', default=True)

    template_id = fields.Many2one(comodel_name='clv.external_sync.template', string='External Sync Template')

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('object_field_pair_uniq',
         'UNIQUE(template_id, external_object_field, local_object_field)',
         u'Error! The Field pair must be unique for a External Sync Template!'
         ),
    ]


class ExternalSyncTemplate(models.Model):
    _inherit = 'clv.external_sync.template'

    object_field_ids = fields.One2many(
        comodel_name='clv.external_sync.template.object_field',
        inverse_name='template_id',
        string='Object Fields'
    )
