# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class PatientAssociateToResidence(models.TransientModel):
    _inherit = 'clv.patient.associate_to_residence'

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

                    new_residence = residence

                else:

                    if self.create_new_residence:

                        Address = self.env['clv.address']
                        address = Address.search([
                            ('street', '=', patient.street),
                            ('street2', '=', patient.street2),
                            ('street_number', '=', patient.street_number),
                            ('street_number2', '=', patient.street_number2),
                        ])
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', 'address_id:', address.id)

                        if address.id is not False:

                            values = {}
                            values['name'] = address.name

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_residence = Residence.create(values)
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_residence:', new_residence)

                            values = {}
                            values['code'] = address.code
                            # values['phase_id'] = address.phase_id.id
                            values['street_name'] = address.street_name
                            values['street'] = address.street
                            values['street2'] = address.street2
                            values['country_id'] = address.country_id.id
                            values['state_id'] = address.state_id.id
                            values['city'] = address.city
                            values['zip'] = address.zip
                            values['phone'] = address.phone
                            values['mobile'] = address.mobile
                            values['email'] = address.email
                            values['street_number'] = address.street_number
                            values['street_number2'] = address.street_number2
                            values['city_id'] = address.city_id.id

                            values['related_address_id'] = address.id

                            values['related_address_is_unavailable'] = False

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_residence.write(values)

                            values = {}
                            values['is_residence'] = True
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            address.write(values)

                            values = {}
                            values['residence_id'] = new_residence.id
                            values['residence_is_unavailable'] = False
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            patient.write(values)

                        else:

                            values = {}
                            values['name'] = patient.address_name

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_residence = Residence.create(values)
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_residence:', new_residence)

                            values = {}
                            # values['code'] = '/'
                            # values['phase_id'] = patient.phase_id.id
                            values['street_name'] = patient.street_name
                            values['street2'] = patient.street2
                            values['street'] = patient.street
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
