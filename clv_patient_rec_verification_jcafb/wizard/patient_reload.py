# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientReload(models.TransientModel):
    _description = 'Patient Reload'
    _name = 'clv.patient.reload'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_reload_rel',
        string='Patients',
        default=_default_patient_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    def do_patient_reload(self):
        self.ensure_one()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if not patient.related_patient_rec_is_unavailable:

                related_patient_rec = patient.related_patient_rec_id
                vals = {}

                if (patient.phase_id.id != related_patient_rec.phase_id.id):

                    vals['phase_id'] = related_patient_rec.phase_id.id

                if (patient.state != related_patient_rec.state):

                    vals['state'] = related_patient_rec.state

                # if (related_patient_rec.category_ids.id is not False):

                m2m_list = []
                count = 0
                for category_id in related_patient_rec.category_ids:
                    m2m_list.append((4, category_id.id))
                    count += 1

                if count > 0:
                    vals['category_ids'] = m2m_list

                # if (related_patient_rec.marker_ids.id is not False):

                m2m_list = []
                count = 0
                for marker_id in related_patient_rec.marker_ids:
                    m2m_list.append((4, marker_id.id))
                    count += 1

                if count > 0:
                    vals['marker_ids'] = m2m_list

                if (patient.name != related_patient_rec.name):

                    vals['name'] = related_patient_rec.name

                if (patient.code != related_patient_rec.code):

                    vals['code'] = related_patient_rec.code

                if (patient.is_absent != related_patient_rec.is_absent):

                    vals['is_absent'] = related_patient_rec.is_absent

                if (patient.gender != related_patient_rec.gender):

                    vals['gender'] = related_patient_rec.gender

                if (patient.birthday != related_patient_rec.birthday):

                    vals['birthday'] = related_patient_rec.birthday

                if (patient.date_death != related_patient_rec.date_death):

                    vals['date_death'] = related_patient_rec.date_death

                if (patient.force_is_deceased != related_patient_rec.force_is_deceased):

                    vals['force_is_deceased'] = related_patient_rec.force_is_deceased

                if self.update_contact_info_data:

                    if (patient.contact_info_is_unavailable != related_patient_rec.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = related_patient_rec.contact_info_is_unavailable

                    if (patient.validate_contact_information != related_patient_rec.validate_contact_information):

                        vals['validate_contact_information'] = related_patient_rec.validate_contact_information

                    if (patient.zip != related_patient_rec.zip):

                        vals['zip'] = related_patient_rec.zip

                    if (patient.street_name != related_patient_rec.street_name):

                        vals['street_name'] = related_patient_rec.street_name

                    if (patient.street_number != related_patient_rec.street_number):

                        vals['street_number'] = related_patient_rec.street_number

                    if (patient.street_number2 != related_patient_rec.street_number2):

                        vals['street_number2'] = related_patient_rec.street_number2

                    if (patient.street2 != related_patient_rec.street2):

                        vals['street2'] = related_patient_rec.street2

                    if (patient.country_id != related_patient_rec.country_id):

                        vals['country_id'] = related_patient_rec.country_id.id

                    if (patient.state_id != related_patient_rec.state_id):

                        vals['state_id'] = related_patient_rec.state_id.id

                    if (patient.city_id != related_patient_rec.city_id):

                        vals['city_id'] = related_patient_rec.city_id.id

                    if (related_patient_rec.phone is not False) and (patient.phone != related_patient_rec.phone):

                        vals['phone'] = related_patient_rec.phone

                    if (related_patient_rec.mobile is not False) and (patient.mobile != related_patient_rec.mobile):

                        vals['mobile'] = related_patient_rec.mobile

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                patient.write(vals)

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True
