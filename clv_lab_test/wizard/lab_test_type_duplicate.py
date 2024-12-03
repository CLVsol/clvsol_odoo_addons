# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class LabTestTypeDuplicate(models.TransientModel):
    _description = 'Lab Test Type Duplicate'
    _name = 'clv.lab_test.type.duplicate'

    def _default_lab_test_type_ids(self):
        return self._context.get('active_ids')
    lab_test_type_ids = fields.Many2many(
        comodel_name='clv.lab_test.type',
        relation='clv_lab_test_type_duplicate_rel',
        string='Lab Test Types',
        default=_default_lab_test_type_ids
    )

    new_name = fields.Char(
        string='New Lab Test Type',
        required=True
    )

    new_code = fields.Char(
        string='New Lab Test Type Code',
        required=True
    )

    new_description = fields.Char(
        string='New Lab Test Type Description',
        required=False
    )

    new_template_file_name_result = fields.Char(
        string='Template File Name (Result)',
        required=False
    )

    new_template_file_name_report = fields.Char(
        string='Template File Name (Report)',
        required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        # defaults['lab_test_type_ids'] = self.env.context['active_ids']

        LabTestType = self.env['clv.lab_test.type']
        lab_test_type_id = self._context.get('active_id')
        lab_test_type = LabTestType.search([
            ('id', '=', lab_test_type_id),
        ])
        defaults['new_name'] = lab_test_type.name
        defaults['new_code'] = lab_test_type.code
        defaults['new_description'] = lab_test_type.description
        defaults['new_template_file_name_result'] = lab_test_type.template_file_name_result
        defaults['new_template_file_name_report'] = lab_test_type.template_file_name_report

        return defaults

    def do_lab_test_type_duplicate(self):
        self.ensure_one()

        LabTestType = self.env['clv.lab_test.type']

        lab_test_type_count = 0
        for lab_test_type in self.lab_test_type_ids:

            lab_test_type_count += 1

            _logger.info(u'%s %s %s', '>>>>>', lab_test_type.code, lab_test_type.name)
            _logger.info(u'%s %s %s', '>>>>>>>>>>', self.new_code, self.new_name)

            values = {
                'name': self.new_name,
                'code': self.new_code,
                'description': self.new_description,
                'template_file_name_result': self.new_template_file_name_result,
                'template_file_name_report': self.new_template_file_name_report,
            }
            new_lab_test_type = LabTestType.create(values)

            export_xls_params = []
            for export_xls_param in lab_test_type.lab_test_export_xls_param_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', export_xls_params)

                parameter = False
                if export_xls_param.parameter is not False:
                    parameter = export_xls_param.parameter.replace(lab_test_type.code, self.new_code)
                export_xls_params.append((0, 0, {'lab_test_type_id': new_lab_test_type.id,
                                                 'display': export_xls_param.display,
                                                 'parameter_type': export_xls_param.parameter_type,
                                                 'parameter': parameter,
                                                 'cell': export_xls_param.cell,
                                                 'col_nr': export_xls_param.col_nr,
                                                 'row_nr': export_xls_param.col_nr,
                                                 }))

            new_lab_test_type.lab_test_export_xls_param_ids = export_xls_params

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', export_xls_params)

            # criteria = []
            # for criterion in lab_test_type.criterion_ids:

            #     criterion_code = False
            #     if criterion.code is not False:
            #         criterion_code = criterion.code.replace(lab_test_type.code, self.new_code)
            #     criteria.append((0, 0, {'code': criterion_code,
            #                             'name': criterion.name,
            #                             'result': criterion.result,
            #                             # 'lab_test_type_id': criterion.lab_test_type_id.id,
            #                             'sequence': criterion.sequence,
            #                             }))

            # new_lab_test_type.criterion_ids = criteria

            # _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', criteria)

        if lab_test_type_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Lab Test Types',
                'res_model': 'clv.lab_test.type',
                'res_id': new_lab_test_type.id,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'target': 'current',
                'context': {'search_default_name': new_lab_test_type.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Lab Test Types',
                'res_model': 'clv.lab_test.type',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'target': 'current',
            }

        return action
