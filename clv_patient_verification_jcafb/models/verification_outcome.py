# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'clv.patient'

    validate_contact_information = fields.Boolean(
        string='Validate Contact Information',
        default=True
    )

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

    verification_marker_ids = fields.Many2many(
        comodel_name='clv.verification.marker',
        relation='clv_patient_verification_marker_rel',
        column1='patient_id',
        column2='verification_marker_id',
        string='Verification Markers'
    )
    verification_marker_names = fields.Char(
        string='Verification Marker Names',
        compute='_compute_verification_marker_names',
        store=True
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

    @api.depends('verification_marker_ids')
    def _compute_verification_marker_names(self):
        for r in self:
            verification_marker_names = False
            for verification_marker in r.verification_marker_ids:
                if verification_marker_names is False:
                    verification_marker_names = verification_marker.name
                else:
                    verification_marker_names = verification_marker_names + ', ' + verification_marker.name
            r.verification_marker_names = verification_marker_names

    def _patient_verification_exec(self):

        VerificationTemplate = self.env['clv.verification.template']
        VerificationOutcome = self.env['clv.verification.outcome']

        model_name = 'clv.patient'

        for patient in self:

            _logger.info(u'%s %s', '>>>>> (patient):', patient.name)

            verification_templates = VerificationTemplate.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('action', '!=', False),
            ])

            for verification_template in verification_templates:

                _logger.info(u'%s %s', '>>>>>>>>>> (verification_template):', verification_template.name)

                verification_outcome = VerificationOutcome.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('res_id', '=', patient.id),
                    ('action', '=', verification_template.action),
                ])

                if verification_outcome.state is False:

                    verification_outcome_values = {}
                    verification_outcome_values['model'] = model_name
                    verification_outcome_values['res_id'] = patient.id
                    verification_outcome_values['res_last_update'] = patient['__last_update']
                    verification_outcome_values['state'] = 'Unknown'
                    # verification_outcome_values['method'] = verification_template.method
                    verification_outcome_values['action'] = verification_template.action
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s',
                                 '(verification_outcome_values):', verification_outcome_values)
                    verification_outcome = VerificationOutcome.create(verification_outcome_values)

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (verification_outcome):', verification_outcome)

                action_call = 'self.env["clv.verification.outcome"].' + \
                    verification_outcome.action + \
                    '(verification_outcome, patient)'

                _logger.info(u'%s %s', '>>>>>>>>>>', action_call)

                if action_call:

                    verification_outcome.state = 'Unknown'
                    verification_outcome.outcome_info = False

                    exec(action_call)

            self.env.cr.commit()

            this_patient = self.env['clv.patient'].with_context({'active_test': False}).search([
                ('id', '=', patient.id),
            ])
            VerificationOutcome._object_verification_outcome_model_object_verification_state_updt(this_patient)

            this_patient._compute_verification_outcome_infos()


class VerificationOutcome(models.Model):
    _inherit = 'clv.verification.outcome'

    def _patient_verification(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_verification = datetime.now()

        PartnerEntityStreetPattern = self.env['clv.partner_entity.street_pattern']
        PartnerEntityStreetPatternMatch = self.env['clv.partner_entity.street_pattern.match']
        PartnerEntityContactInformationPattern = self.env['clv.partner_entity.contact_information_pattern']
        PartnerEntityContactInformationPatternMatch = self.env['clv.partner_entity.contact_information_pattern.match']

        street_ref_id = model_object._name + ',' + str(model_object.id)
        PartnerEntityStreetPatternMatch.search([
            ('ref_id', '=', street_ref_id),
        ]).unlink()

        contact_information_ref_id = model_object._name + ',' + str(model_object.id)
        PartnerEntityContactInformationPatternMatch.search([
            ('ref_id', '=', contact_information_ref_id),
        ]).unlink()

        state = 'Ok'
        outcome_info = ''

        if model_object.contact_info_is_unavailable:

            if model_object.street_name is not False:

                outcome_info = _('"Contact Information" should not be set.\n')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            # outcome_info = _('"Contact Information is Unavailable" should not be set.\n')
            # state = self._get_verification_outcome_state(state, 'Error (L0)')

        else:

            if model_object.code is False:

                outcome_info += _('"Patient Code" is missing.\n')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            if model_object.street_name is False:

                outcome_info += _('"Contact Information" is missing.\n')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            # if model_object.reg_state not in ['done', 'canceled']:
            if model_object.validate_contact_information is True:

                street_patern = PartnerEntityStreetPattern.search([
                    ('street', '=', model_object.street_name),
                    ('street2', '=', model_object.street2),
                ])

                if street_patern.street is False:

                    outcome_info += _('"Street Pattern" was not recognised.') + \
                        ' (' + str(model_object.street_name) + ' [' + str(model_object.street2) + '])\n'
                    state = self._get_verification_outcome_state(state, 'Warning (L0)')

                else:

                    values = {
                        'street_pattern_id': street_patern.id,
                        'ref_id': street_ref_id,
                    }
                    PartnerEntityStreetPatternMatch.create(values)

                if (model_object.zip is False) or \
                   (model_object.street_name is False) or \
                   (model_object.street2 is False) or \
                   (model_object.country_id is False) or \
                   (model_object.state_id is False) or \
                   (model_object.city_id is False):

                    outcome_info += _('Please, verify "Contact Information (Street)" data.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L0)')

                # if (model_object.zip is False) or \
                #    (model_object.street_name is False) or \
                #    (model_object.street_number is False) or \
                #    (model_object.street_number2 is False) or \
                #    (model_object.street2 is False) or \
                #    (model_object.country_id is False) or \
                #    (model_object.state_id is False) or \
                #    (model_object.city_id is False):

                #     outcome_info += _('Please, verify "Contact Information (Complement)" data.\n')
                #     state = self._get_verification_outcome_state(state, 'Warning (L0)')

                # contact_information_patern = PartnerEntityContactInformationPattern.search([
                #     ('street', '=', model_object.street_name),
                #     ('street_number', '=', model_object.street_number),
                #     ('street_number2', '=', model_object.street_number2),
                #     ('street2', '=', model_object.street2),
                # ])

                if (model_object.street_number2 is False) or (model_object.street_number2 == ''):
                    contact_information_patern = PartnerEntityContactInformationPattern.search([
                        ('street', '=', model_object.street_name),
                        ('street_number', '=', model_object.street_number),
                        # ('street_number2', '=', model_object.street_number2),
                        '|',
                        ('street_number2', '=', False),
                        ('street_number2', '=', ''),
                        ('street2', '=', model_object.street2),
                    ])
                else:
                    contact_information_patern = PartnerEntityContactInformationPattern.search([
                        ('street', '=', model_object.street_name),
                        ('street_number', '=', model_object.street_number),
                        ('street_number2', '=', model_object.street_number2),
                        ('street2', '=', model_object.street2),
                    ])

                if contact_information_patern.street is False:

                    outcome_info += _('"Contact Information Pattern" was not recognised.') + \
                        ' (' + str(model_object.address_name) + ')\n'
                    state = self._get_verification_outcome_state(state, 'Warning (L0)')

                else:

                    values = {
                        'contact_information_pattern_id': contact_information_patern.id,
                        'ref_id': contact_information_ref_id,
                    }
                    PartnerEntityContactInformationPatternMatch.create(values)

        # if model_object.reg_state not in ['ready', 'done', 'canceled']:
        if model_object.reg_state not in ['canceled']:

            if model_object.gender is False:

                outcome_info += _('"Gender" is missing.\n')
                state = self._get_verification_outcome_state(state, 'Warning (L0)')

            if model_object.birthday is False:

                outcome_info += _('"Date of Birth" is missing.\n')
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

    def _patient_verification_patient_aux(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_verification = datetime.now()

        state = 'Ok'
        outcome_info = ''

        patient_aux_ids = model_object.patient_aux_ids

        # if len(patient_aux_ids) == 0:
        #     outcome_info = _('Missing related "Patient (Aux)" register.')
        #     state = self._get_verification_outcome_state(state, 'Error (L1)')

        if len(patient_aux_ids) > 1:
            outcome_info = _('There are more than one related "Patient (Aux)" register.')
            state = self._get_verification_outcome_state(state, 'Error (L1)')

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

    def _patient_verification_residence(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_verification = datetime.now()

        residence = model_object.residence_id

        state = 'Ok'
        outcome_info = ''

        if model_object.residence_is_unavailable:

            if residence.id is not False:

                outcome_info = _('"Residence" should not be set\n.')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            # outcome_info = _('"Residence is Unavailable" should not be set.\n')
            # state = self._get_verification_outcome_state(state, 'Error (L0)')

        else:

            if residence.id is not False:

                if (model_object.zip != residence.zip) or \
                   (model_object.street_name != residence.street_name) or \
                   (model_object.street_number != residence.street_number) or \
                   (model_object.street_number2 != residence.street_number2) or \
                   (model_object.street2 != residence.street2) or \
                   (model_object.country_id != residence.country_id) or \
                   (model_object.state_id != residence.state_id) or \
                   (model_object.city_id != residence.city_id):

                    outcome_info += _('Residence "Contact Information" mismatch.')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if residence.phase_id.id != model_object.phase_id.id:

                    outcome_info += _('Residence "Phase" mismatch.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if residence.state != model_object.state:

                    if not ((residence.state == 'selected') and (model_object.state == 'waiting')):

                        outcome_info += _('Residence "State" mismatch.\n')
                        state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if residence.employee_id.id != model_object.employee_id.id:

                    outcome_info += _('Residence "Responsible Empĺoyee" mismatch.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if model_object.residence_id.verification_state != 'Ok':

                    outcome_info += _('Residence "Verification State" is "') + \
                        model_object.residence_id.verification_state + '".\n'
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

            else:

                outcome_info = _('Missing "Residence".')
                state = self._get_verification_outcome_state(state, 'Warning (L1)')

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
