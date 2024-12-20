# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PatientRecContactInformationPatternAdd(models.TransientModel):
    _description = 'Patient (Rec) Contact Information Pattern Add'
    _name = 'clv.patient_rec.contact_information_pattern_add'

    def _default_patient_rec_ids(self):
        return self._context.get('active_ids')
    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_contact_information_pattern_add_rel',
        string='Patients (Rec)',
        default=_default_patient_rec_ids)
    count_patients_aux = fields.Integer(
        string='Number of Patients (Rec)',
        compute='_compute_count_patients_aux',
        store=False
    )

    patient_rec_verification_exec = fields.Boolean(
        string='Patient (Rec) Verification Execute',
        default=True,
    )

    @api.depends('patient_rec_ids')
    def _compute_count_patients_aux(self):
        for r in self:
            r.count_patients_aux = len(r.patient_rec_ids)

    def do_patient_rec_contact_information_pattern_add(self):
        self.ensure_one()

        PartnerEntityContactInformationPattern = self.env['clv.partner_entity.contact_information_pattern']

        for patient_rec in self.patient_rec_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (patient_rec):', patient_rec.name)

            street_patern = PartnerEntityContactInformationPattern.search([
                ('street', '=', patient_rec.street_name),
                ('street_number', '=', patient_rec.street_number),
                ('street_number2', '=', patient_rec.street_number2),
                ('street2', '=', patient_rec.street2),
            ])

            if street_patern.street is False:

                values = {}
                values['street'] = patient_rec.street_name
                values['street_number'] = patient_rec.street_number
                values['street_number2'] = patient_rec.street_number2
                values['street2'] = patient_rec.street2
                values['active'] = True
                PartnerEntityContactInformationPattern.create(values)

            if self.patient_rec_verification_exec:
                patient_rec._patient_rec_verification_exec()

        return True
