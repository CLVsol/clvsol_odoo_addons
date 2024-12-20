# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import fields, models, _

_logger = logging.getLogger(__name__)


class LabTestTypeExportXlsParam(models.Model):
    _inherit = 'clv.lab_test.export_xls.param'

    verification_outcome_ids = fields.One2many(
        string='Verification Outcomes',
        comodel_name='clv.verification.outcome',
        compute='_compute_verification_outcome_ids_and_count',
    )
    count_verification_outcomes = fields.Integer(
        string='Verification Outcomes (count)',
        compute='_compute_verification_outcome_ids_and_count',
    )
    count_verification_outcomes_2 = fields.Integer(
        string='Verification Outcomes 2 (count)',
        compute='_compute_verification_outcome_ids_and_count',
    )
    verification_outcome_infos = fields.Char(
        string='Verification Outcome Informations',
        compute='_compute_verification_outcome_infos',
        store=True
    )

    verification_state = fields.Char(
        string='Verification State',
        default='Unknown',
        readonly=True
    )

    def _compute_verification_outcome_ids_and_count(self):
        for record in self:

            search_domain = [
                ('model', '=', self._name),
                ('res_id', '=', record.id),
            ]

            verification_outcomes = self.env['clv.verification.outcome'].search(search_domain)

            record.count_verification_outcomes = len(verification_outcomes)
            record.count_verification_outcomes_2 = len(verification_outcomes)
            record.verification_outcome_ids = [(6, 0, verification_outcomes.ids)]

    def _compute_verification_outcome_infos(self):
        for record in self:

            search_domain = [
                ('model', '=', self._name),
                ('res_id', '=', record.id),
            ]

            verification_outcomes = self.env['clv.verification.outcome'].search(search_domain)

            verification_outcome_infos = False
            for verification_outcome in verification_outcomes:
                if verification_outcome.outcome_info is not False:
                    if verification_outcome_infos is False:
                        verification_outcome_infos = verification_outcome.outcome_info
                    else:
                        verification_outcome_infos = \
                            verification_outcome_infos + ', ' + verification_outcome.outcome_info
            record.verification_outcome_infos = verification_outcome_infos

    def _lab_test_export_xls_param_verification_exec(self):

        VerificationTemplate = self.env['clv.verification.template']
        VerificationOutcome = self.env['clv.verification.outcome']

        model_name = 'clv.lab_test.export_xls.param'

        for lab_test_export_xls_param in self:

            _logger.info(u'%s %s', '>>>>> (lab_test_export_xls_param):', lab_test_export_xls_param)

            verification_templates = VerificationTemplate.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('action', '!=', False),
            ])

            for verification_template in verification_templates:

                _logger.info(u'%s %s', '>>>>>>>>>> (verification_template):', verification_template.name)

                verification_outcome = VerificationOutcome.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('res_id', '=', lab_test_export_xls_param.id),
                    ('action', '=', verification_template.action),
                ])

                if verification_outcome.state is False:

                    verification_outcome_values = {}
                    verification_outcome_values['model'] = model_name
                    verification_outcome_values['res_id'] = lab_test_export_xls_param.id
                    verification_outcome_values['res_last_update'] = lab_test_export_xls_param['__last_update']
                    verification_outcome_values['state'] = 'Unknown'
                    # verification_outcome_values['method'] = verification_template.method
                    verification_outcome_values['action'] = verification_template.action
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s',
                                 '(verification_outcome_values):', verification_outcome_values)
                    verification_outcome = VerificationOutcome.create(verification_outcome_values)

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (verification_outcome):', verification_outcome)

                action_call = 'self.env["clv.verification.outcome"].' + \
                    verification_outcome.action + \
                    '(verification_outcome, lab_test_export_xls_param)'

                _logger.info(u'%s %s', '>>>>>>>>>>', action_call)

                if action_call:

                    verification_outcome.state = 'Unknown'
                    verification_outcome.outcome_info = False

                    exec(action_call)

            self.env.cr.commit()

            this_lab_test_export_xls_param = \
                self.env['clv.lab_test.export_xls.param'].with_context({'active_test': False}).search([
                    ('id', '=', lab_test_export_xls_param.id),
                ])
            VerificationOutcome._object_verification_outcome_model_object_verification_state_updt(this_lab_test_export_xls_param)

            this_lab_test_export_xls_param._compute_verification_outcome_infos()


class VerificationOutcome(models.Model):
    _inherit = 'clv.verification.outcome'

    def _lab_test_export_xls_param_verification(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object)

        date_verification = datetime.now()

        LabTestTypeExportXlsParamPattern = self.env['clv.lab_test.export_xls.param.pattern']

        state = 'Ok'
        outcome_info = ''

        if model_object.parameter_type == 'variable_name':

            export_xls_param = LabTestTypeExportXlsParamPattern.search([
                ('display', '=', model_object.display),
                ('parameter_type', '=', model_object.parameter_type),
                ('parameter', '=', model_object.parameter),
            ])

            if export_xls_param.parameter is False:

                outcome_info += _('"Lab Test Export XLS Parameter Pattern" was not recognised.') + \
                    ' (' + str(model_object.display) + \
                    ', ' + str(model_object.parameter_type) + \
                    ', ' + str(model_object.parameter) + ')\n'
                state = self._get_verification_outcome_state(state, 'Warning (L0)')

        if outcome_info == '':
            outcome_info = False

        self._object_verification_outcome_updt(
            verification_outcome, state, outcome_info, date_verification, model_object
        )

        verification_values = {}
        verification_values['date_verification'] = date_verification
        verification_values['outcome_info'] = outcome_info
        verification_values['state'] = state
        verification_outcome.write(verification_values)
