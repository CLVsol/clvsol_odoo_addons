# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientAssociateToResidence(models.TransientModel):
    _description = 'Patient Associate to Residence'
    _name = 'clv.patient.associate_to_residence'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_associate_to_residence_rel',
        string='Patients',
        default=_default_patient_ids
    )

    create_new_residence = fields.Boolean(
        string='Create new Residence',
        default=False
    )

    residence_verification_exec = fields.Boolean(
        string='Residence Verification Execute',
        default=True,
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

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

    def do_patient_associate_to_residence(self):
        self.ensure_one()

        patient_count = 0
        for patient in self.patient_ids:

            patient_count += 1

            _logger.info(u'%s %s %s', '>>>>>', patient_count, patient.name)

            if patient.contact_info_is_unavailable is False:

                Residence = self.env['clv.residence']
                residence = Residence.search([
                    ('street', '=', patient.street),
                    ('street2', '=', patient.street2),
                    ('street_number', '=', patient.street_number),
                    ('street_number2', '=', patient.street_number2),
                ])
                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'residence_id:', residence.id)

                if residence.id is not False:

                    values = {}
                    values['residence_id'] = residence.id
                    values['residence_is_unavailable'] = False
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    patient.write(values)

                else:

                    if self.create_new_residence:

                        values = {}
                        values['name'] = patient.address_name

                        _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                        new_residence = Residence.create(values)
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_residence:', new_residence)

                        values = {}
                        # values['code'] = '/'
                        # values['phase_id'] = patient.phase_id.id
                        values['street_name'] = patient.street_name
                        values['street'] = patient.street
                        values['street2'] = patient.street2
                        values['country_id'] = patient.country_id.id
                        values['state_id'] = patient.state_id.id
                        values['city'] = patient.city
                        values['zip'] = patient.zip
                        values['phone'] = patient.phone
                        values['mobile'] = patient.mobile
                        values['email'] = patient.email
                        values['street_number'] = patient.street_number
                        values['street_number2'] = patient.street_number2
                        values['city_id'] = patient.city_id.id
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                        new_residence.write(values)

                        values = {}
                        values['residence_id'] = new_residence.id
                        values['residence_is_unavailable'] = False
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                        patient.write(values)

            if self.residence_verification_exec:
                new_residence._residence_verification_exec()

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True
