# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ModelExportCreateTemplate(models.TransientModel):
    _description = 'Model Export Create Template'
    _name = 'clv.model_export.create_template'

    def _default_model_export_ids(self):
        return self._context.get('active_ids')
    model_export_ids = fields.Many2many(
        comodel_name='clv.model_export',
        relation='clv_model_export_create_template_rel',
        string='Model Exports',
        default=_default_model_export_ids
    )

    new_name = fields.Char(
        string='New Model Export Template Name',
        required=True
    )

    new_label = fields.Char(
        string='New Model Export Template Label',
        required=True
    )

    @api.model
    def default_get(self, field_names):

        defaults = super(ModelExportCreateTemplate, self).default_get(field_names)

        ModelExport = self.env['clv.model_export']
        model_export_id = self._context.get('active_id')
        model_export = ModelExport.search([
            ('id', '=', model_export_id),
        ])
        defaults['new_name'] = model_export.name
        defaults['new_label'] = model_export.label

        return defaults

    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def do_model_export_create_template(self):
        self.ensure_one()

        ModelExportTemplate = self.env['clv.model_export.template']
        ModelExportTemplateField = self.env['clv.model_export.template.field']
        ModelExportTemplateDocumentItem = self.env['clv.model_export.template.document_item']

        ModelExport = self.env['clv.model_export']
        # ModelExportField = self.env['clv.model_export.field']
        ModelExportDocumentItem = self.env['clv.model_export.document_item']
        ModelExportLabTestCriterion = self.env['clv.model_export.lab_test_criterion']

        for model_export in self.model_export_ids:

            _logger.info(u'%s %s %s %s', '>>>>>',
                         model_export.name, model_export.label, model_export.template_id.name)
            _logger.info(u'%s %s %s', '>>>>>>>>>>', self.new_name, self.new_label)

            values = {
                'name': self.new_name,
                'label': self.new_label,
                'model_id': model_export.model_id.id,
                'export_type': model_export.export_type,
            }
            if hasattr(ModelExport, 'use_document_items'):
                values['use_document_items'] = model_export.use_document_items
            if hasattr(ModelExport, 'use_lab_test_criteria'):
                values['use_lab_test_criteria'] = model_export.use_lab_test_criteria
            new_model_export = ModelExportTemplate.create(values)

            for model_export_field in model_export.model_export_field_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', model_export_field.field_id.name)

                values = {
                    'sequence': model_export_field.sequence,
                    'name': model_export_field.name,
                    'model_export_template_id': new_model_export.id,
                    'model_export_display': model_export_field.model_export_display,
                    'field_id': model_export_field.field_id.id,
                }
                ModelExportTemplateField.create(values)

            if hasattr(ModelExport, 'use_document_items'):

                model_export_document_items = ModelExportDocumentItem.search([
                    ('model_export_id', '=', model_export.id),
                ])
                for model_export_document_item in model_export_document_items:
                    _logger.info(u'%s %s', '>>>>>>>>>>>>>>>',
                                 model_export_document_item.document_item_id.name)
                    values = {
                        'sequence': model_export_document_item.sequence,
                        'name': model_export_document_item.name,
                        'model_export_template_id': new_model_export.id,
                        'model_export_display': model_export_document_item.model_export_display,
                        'document_item_id': model_export_document_item.document_item_id.id,
                    }
                    ModelExportTemplateDocumentItem.create(values)

            if hasattr(ModelExport, 'use_lab_test_criteria'):

                ModelExportTemplateLabTestCriterion = self.env['clv.model_export.template.lab_test_criterion']
                model_export_lab_test_criteria = ModelExportLabTestCriterion.search([
                    ('model_export_id', '=', model_export.id),
                ])
                for model_export_lab_test_criterion in model_export_lab_test_criteria:
                    _logger.info(u'%s %s', '>>>>>>>>>>>>>>>',
                                 model_export_lab_test_criterion.lab_test_criterion_id.name)
                    values = {
                        'sequence': model_export_lab_test_criterion.sequence,
                        'name': model_export_lab_test_criterion.name,
                        'model_export_template_id': new_model_export.id,
                        'model_export_display': model_export_lab_test_criterion.model_export_display,
                        'lab_test_criterion_id': model_export_lab_test_criterion.lab_test_criterion_id.id,
                    }
                    ModelExportTemplateLabTestCriterion.create(values)

        return True
