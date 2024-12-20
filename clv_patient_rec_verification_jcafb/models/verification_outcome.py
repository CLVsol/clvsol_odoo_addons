# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class PatientRec(models.Model):
    _inherit = 'clv.patient_rec'

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
        relation='clv_patient_rec_verification_marker_rel',
        column1='patient_rec_id',
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

    def _patient_rec_verification_exec(self):

        VerificationTemplate = self.env['clv.verification.template']
        VerificationOutcome = self.env['clv.verification.outcome']

        model_name = 'clv.patient_rec'

        for patient_rec in self:

            _logger.info(u'%s %s', '>>>>> (patient_rec):', patient_rec.name)

            verification_templates = VerificationTemplate.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('action', '!=', False),
            ])

            for verification_template in verification_templates:

                _logger.info(u'%s %s', '>>>>>>>>>> (verification_template):', verification_template.name)

                verification_outcome = VerificationOutcome.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('res_id', '=', patient_rec.id),
                    ('action', '=', verification_template.action),
                ])

                if verification_outcome.state is False:

                    verification_outcome_values = {}
                    verification_outcome_values['model'] = model_name
                    verification_outcome_values['res_id'] = patient_rec.id
                    verification_outcome_values['res_last_update'] = patient_rec['__last_update']
                    verification_outcome_values['state'] = 'Unknown'
                    # verification_outcome_values['method'] = verification_template.method
                    verification_outcome_values['action'] = verification_template.action
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s',
                                 '(verification_outcome_values):', verification_outcome_values)
                    verification_outcome = VerificationOutcome.create(verification_outcome_values)

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (verification_outcome):', verification_outcome)

                action_call = 'self.env["clv.verification.outcome"].' + \
                    verification_outcome.action + \
                    '(verification_outcome, patient_rec)'

                _logger.info(u'%s %s', '>>>>>>>>>> (action_call):', action_call)

                if action_call:

                    verification_outcome.state = 'Unknown'
                    verification_outcome.outcome_info = False

                    exec(action_call)

            self.env.cr.commit()

            this_patient_rec = self.env['clv.patient_rec'].with_context({'active_test': False}).search([
                ('id', '=', patient_rec.id),
            ])
            VerificationOutcome._object_verification_outcome_model_object_verification_state_updt(this_patient_rec)

            this_patient_rec._compute_verification_outcome_infos()


class VerificationOutcome(models.Model):
    _inherit = 'clv.verification.outcome'

    def _patient_rec_verification(self, verification_outcome, model_object):

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

        else:

            if model_object.code is False:

                outcome_info += _('"Patient Code" is missing.\n')
                state = self._get_verification_outcome_state(state, 'Warning (L0)')

            if model_object.street_name is False:

                outcome_info += _('"Contact Information" is missing.\n')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            # if model_object.reg_state not in ['verified', 'ready', 'done', 'canceled']:
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

                # contact_information_pattern = PartnerEntityContactInformationPattern.search([
                #     ('street', '=', model_object.street_name),
                #     ('street_number', '=', model_object.street_number),
                #     ('street_number2', '=', model_object.street_number2),
                #     ('street2', '=', model_object.street2),
                # ])

                if (model_object.street_number2 is False) or (model_object.street_number2 == ''):
                    contact_information_pattern = PartnerEntityContactInformationPattern.search([
                        ('street', '=', model_object.street_name),
                        ('street_number', '=', model_object.street_number),
                        # ('street_number2', '=', model_object.street_number2),
                        '|',
                        ('street_number2', '=', False),
                        ('street_number2', '=', ''),
                        ('street2', '=', model_object.street2),
                    ])
                else:
                    contact_information_pattern = PartnerEntityContactInformationPattern.search([
                        ('street', '=', model_object.street_name),
                        ('street_number', '=', model_object.street_number),
                        ('street_number2', '=', model_object.street_number2),
                        ('street2', '=', model_object.street2),
                    ])

                if contact_information_pattern.street is False:

                    outcome_info += _('"Contact Information Pattern" was not recognised.') + \
                        ' (' + str(model_object.address_name) + ')\n'
                    state = self._get_verification_outcome_state(state, 'Warning (L0)')

                else:

                    values = {
                        'contact_information_pattern_id': contact_information_pattern.id,
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

        if (model_object.is_absent is True) and (model_object.state not in ['unavailable']):

            outcome_info += _('"Patient (Rec) State" should be "Unavailable".\n')
            state = self._get_verification_outcome_state(state, 'Error (L0)')

        if (model_object.is_deceased is True) and (model_object.state not in ['unavailable']):

            outcome_info += _('"Patient (Rec) State" should be "Unavailable".\n')
            state = self._get_verification_outcome_state(state, 'Error (L0)')

        if outcome_info == '':
            outcome_info = False

        self._object_verification_outcome_updt(
            verification_outcome, state, outcome_info, date_verification, model_object
        )

    def _patient_verification_related_patient_rec(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_verification = datetime.now()

        related_patient_rec = model_object.related_patient_rec_id

        state = 'Ok'
        outcome_info = ''

        if model_object.related_patient_rec_is_unavailable:

            outcome_info = _('"Related Patient (Rec) is Unavailable" should not be set.\n')
            state = self._get_verification_outcome_state(state, 'Error (L1)')

        else:

            if related_patient_rec.id is not False:

                if (model_object.name != related_patient_rec.name):

                    outcome_info += _('"Name" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.code != related_patient_rec.code):

                    outcome_info += _('"Patient Code" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.is_absent != related_patient_rec.is_absent):

                    outcome_info += _('"Is Absent" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.gender != related_patient_rec.gender):

                    outcome_info += _('"Gender" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.estimated_age != related_patient_rec.estimated_age):

                    outcome_info += _('"Estimated Age" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.birthday != related_patient_rec.birthday):

                    outcome_info += _('"Date of Birth" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.force_is_deceased != related_patient_rec.force_is_deceased):

                    outcome_info += _('"Force Is Deceased" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.date_death != related_patient_rec.date_death):

                    outcome_info += _('"Deceased Date" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.phase_id != related_patient_rec.phase_id):

                    outcome_info += _('"Phase" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.state != related_patient_rec.state):

                    outcome_info += _('"State" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.zip != related_patient_rec.zip) or \
                   (model_object.street_name != related_patient_rec.street_name) or \
                   (model_object.street_number != related_patient_rec.street_number) or \
                   (model_object.street_number2 != related_patient_rec.street_number2) or \
                   (model_object.street2 != related_patient_rec.street2) or \
                   (model_object.country_id != related_patient_rec.country_id) or \
                   (model_object.state_id != related_patient_rec.state_id) or \
                   (model_object.city_id != related_patient_rec.city_id):

                    outcome_info += _('"Contact Information (Address)" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if (model_object.validate_contact_information != related_patient_rec.validate_contact_information) or \
                   (model_object.contact_info_is_unavailable != related_patient_rec.contact_info_is_unavailable):

                    outcome_info += _('"Contact Information (Address)" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if ((model_object.phone is not False) and (model_object.phone != related_patient_rec.phone)) or \
                   ((model_object.mobile is not False) and (model_object.mobile != related_patient_rec.mobile)) or \
                   ((model_object.email is not False) and (model_object.email != related_patient_rec.email)):

                    outcome_info += _('"Contact Information (Phones)" has changed.\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                # if (model_object.global_tag_ids.id is not False):

                related_patient_rec_global_tag_ids = []
                for global_tag_id in related_patient_rec.global_tag_ids:
                    related_patient_rec_global_tag_ids.append(global_tag_id.id)

                count_new_global_tag_ids = 0
                for global_tag_id in model_object.global_tag_ids:
                    if global_tag_id.id not in related_patient_rec_global_tag_ids:
                        count_new_global_tag_ids += 1

                if count_new_global_tag_ids > 0:
                    outcome_info += _('Added "Global Tag(s)".\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                # if (model_object.category_ids.id is not False):

                related_patient_rec_category_ids = []
                for category_id in related_patient_rec.category_ids:
                    related_patient_rec_category_ids.append(category_id.id)

                count_new_category_ids = 0
                for category_id in model_object.category_ids:
                    if category_id.id not in related_patient_rec_category_ids:
                        count_new_category_ids += 1

                if count_new_category_ids > 0:
                    outcome_info += _('Added "Patient Category(ies)".\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                # if (related_patient_rec.category_ids.id is not False):

                model_object_category_ids = []
                for category_id in model_object.category_ids:
                    model_object_category_ids.append(category_id.id)

                count_new_category_ids = 0
                for category_id in related_patient_rec.category_ids:
                    if category_id.id not in model_object_category_ids:
                        count_new_category_ids += 1

                if count_new_category_ids > 0:
                    outcome_info += _('Removed "Patient Category(ies)".\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                # if (model_object.marker_ids.id is not False):

                related_patient_rec_marker_ids = []
                for marker_id in related_patient_rec.marker_ids:
                    related_patient_rec_marker_ids.append(marker_id.id)

                count_new_marker_ids = 0
                for marker_id in model_object.marker_ids:
                    if marker_id.id not in related_patient_rec_marker_ids:
                        count_new_marker_ids += 1

                if count_new_marker_ids > 0:
                    outcome_info += _('Added "Patient Marker(s)".\n')
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

                if model_object.related_patient_rec_id.verification_state != 'Ok':

                    outcome_info += _('Related Patient (Rec) "Verification State" is "') + \
                        model_object.related_patient_rec_id.verification_state + '".\n'
                    state = self._get_verification_outcome_state(state, 'Warning (L1)')

            else:

                outcome_info = _('Missing "Related Patient (Rec)".\n')
                state = self._get_verification_outcome_state(state, 'Error (L1)')

        if outcome_info == '':
            outcome_info = False

        self._object_verification_outcome_updt(
            verification_outcome, state, outcome_info, date_verification, model_object
        )
