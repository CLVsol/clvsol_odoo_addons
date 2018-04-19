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


class ModelExport(models.Model):
    _description = 'Model Export'
    _name = 'clv.model_export'
    _inherit = 'clv.object.model_export', 'clv.code.model'

    code = fields.Char(string='Model Export Code', required=False, default='/')
    code_sequence = fields.Char(default='clv.export.code')

    template_id = fields.Many2one(
        comodel_name='clv.model_export.template',
        string='Model Export Template',
        required=False,
        ondelete='restrict'
    )

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.onchange('template_id')
    def onchange_template_id(self):
        # ModelExportField = self.env['clv.model_export.field']
        if self.template_id:
            self.name = self.template_id.name
            self.label = self.template_id.label
            self.model_id = self.template_id.model_id
            self.notes = self.template_id.notes
            # for model_export_field in self.model_export_field_ids:
            #     print '>>>>>', model_export_field
            # model_export_field_ids = []
            # for model_export_template_field in self.template_id.model_export_template_field_ids:
            #     print '>>>>>', model_export_template_field
            #     values = {
            #         'name': model_export_template_field.name,
            #         'model_export_id': self.id,
            #         'field_id': model_export_template_field.field_id.id,
            #         'sequence': model_export_template_field.sequence,
            #     }
            #     new_model_export_template_field = ModelExportField.create(values)
            #     model_export_field_ids += [new_model_export_template_field.id]
            # self.model_export_field_ids = model_export_field_ids

    @api.model
    def create(self, values):

        ModelExportField = self.env['clv.model_export.field']

        new_model_export = super(ModelExport, self).create(values)

        model_export_field_ids = []
        for model_export_template_field in new_model_export.template_id.model_export_template_field_ids:
            values = {
                'name': model_export_template_field.name,
                'model_export_id': new_model_export.id,
                'field_id': model_export_template_field.field_id.id,
                'sequence': model_export_template_field.sequence,
            }
            new_model_export_template_field = ModelExportField.create(values)
            model_export_field_ids += [new_model_export_template_field.id]

        return new_model_export

    @api.multi
    def write(self, values):

        ModelExportField = self.env['clv.model_export.field']

        res = super(ModelExport, self).write(values)

        if 'template_id' in values:

            for model_export_field in self.model_export_field_ids:
                model_export_field.unlink()

            model_export_field_ids = []
            for model_export_template_field in self.template_id.model_export_template_field_ids:
                values = {
                    'name': model_export_template_field.name,
                    'model_export_id': self.id,
                    'field_id': model_export_template_field.field_id.id,
                    'sequence': model_export_template_field.sequence,
                }
                new_model_export_template_field = ModelExportField.create(values)
                model_export_field_ids += [new_model_export_template_field.id]

        return res


class ModelExportTemplate(models.Model):
    _inherit = 'clv.model_export.template'

    model_export_ids = fields.One2many(
        comodel_name='clv.model_export',
        inverse_name='template_id',
        string='Model Exports'
    )
    count_model_exports = fields.Integer(
        string='Model Exports',
        compute='_compute_count_model_exports',
        store=True
    )

    @api.multi
    @api.depends('model_export_ids')
    def _compute_count_model_exports(self):
        for r in self:
            r.count_model_exports = len(r.model_export_ids)
