# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResidenceLabTestResultSetup_2(models.TransientModel):
    _description = 'Residence Lab Test Result Setup 2'
    _name = 'clv.residence.lab_test.result.setup_2'

    def _default_residence_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='clv_residence_residence_lab_test_result_setup_2_rel',
        string='Residences',
        default=_default_residence_ids
    )

    # lab_test_type_ids = fields.Many2many(
    #     comodel_name='clv.lab_test.type',
    #     relation='clv_lab_test_type_residence_lab_test_result_setup_2_rel',
    #     string='Lab Test Types'
    # )

    lab_test_type_id = fields.Many2one(
        comodel_name='clv.lab_test.type',
        string='Lab Test Types'
    )

    lab_test_result_code = fields.Char(string='Lab Test Result Code', required=True, default='/')

    def _default_phase_id(self):
        phase_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip())
        return phase_id
    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        default=_default_phase_id,
        ondelete='restrict'
    )

    def do_residence_lab_test_result_setup_2(self):
        self.ensure_one()

        LabTestResult = self.env['clv.lab_test.result']

        for residence in self.residence_ids:

            _logger.info(u'%s %s', '>>>>>', residence.name)

            # for lab_test_type in self.lab_test_type_ids:

            lab_test_type = self.lab_test_type_id

            # m2m_list = []
            # m2m_list.append((4, lab_test_type.id))

            ref_id = residence._name + ',' + str(residence.id)

            # _logger.info(u'%s %s %s', '>>>>>>>>>>', ref_id, m2m_list)
            _logger.info(u'%s %s %s', '>>>>>>>>>>', ref_id, lab_test_type)

            lab_test_result = LabTestResult.search([
                ('lab_test_type_id', '=', lab_test_type.id),
                ('ref_id', '=', ref_id),
            ])

            if lab_test_result.id is False:

                values = {
                    'code_sequence': 'clv.lab_test.result.code',
                    'code': self.lab_test_result_code,
                    # 'lab_test_type_ids': m2m_list,
                    'lab_test_type_id': lab_test_type.id,
                    'survey_id': lab_test_type.survey_id.id,
                    'ref_id': ref_id,
                    'phase_id': self.phase_id.id,
                }
                new_lab_test_result = LabTestResult.create(values)

                _logger.info(u'%s %s', '>>>>>>>>>>', new_lab_test_result.code)

        return True
