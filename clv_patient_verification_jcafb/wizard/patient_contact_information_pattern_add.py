# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PatientContactInformationPatternAdd(models.TransientModel):
    _description = 'Patient Contact Information Pattern Add'
    _name = 'clv.patient.contact_information_pattern_add'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_contact_information_pattern_add_rel',
        string='Patients',
        default=_default_patient_ids)
    count_patients = fields.Integer(
        string='Number of Patients',
        compute='_compute_count_patients',
        store=False
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    @api.depends('patient_ids')
    def _compute_count_patients(self):
        for r in self:
            r.count_patients = len(r.patient_ids)

    def do_patient_contact_information_pattern_add(self):
        self.ensure_one()

        PartnerEntityContactInformationPattern = self.env['clv.partner_entity.contact_information_pattern']

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (patient):', patient.name)

            street_patern = PartnerEntityContactInformationPattern.search([
                ('street', '=', patient.street_name),
                ('street_number', '=', patient.street_number),
                ('street_number2', '=', patient.street_number2),
                ('street2', '=', patient.street2),
            ])

            if street_patern.street is False:

                values = {}
                values['street'] = patient.street_name
                values['street_number'] = patient.street_number
                values['street_number2'] = patient.street_number2
                values['street2'] = patient.street2
                values['active'] = True
                PartnerEntityContactInformationPattern.create(values)

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True
