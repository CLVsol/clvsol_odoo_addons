# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientRelatePatienRectUpdt(models.TransientModel):
    _description = 'Patient Related Patient (Rec) Update'
    _name = 'clv.patient.related_patient_rec_updt'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_related_patient_rec_updt_rel',
        string='Patients',
        default=_default_patient_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    related_patient_rec_verification_exec = fields.Boolean(
        string='Related Patient (Rec) Verification Execute',
        default=True,
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    def do_patient_related_patient_rec_updt(self):
        self.ensure_one()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if not patient.related_patient_rec_is_unavailable:

                related_patient_rec = patient.related_patient_rec_id
                vals = {}

                if (patient.phase_id != related_patient_rec.phase_id):

                    vals['phase_id'] = patient.phase_id.id

                if (patient.state != related_patient_rec.state):

                    vals['state'] = patient.state

                if (patient.global_tag_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in patient.global_tag_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['global_tag_ids'] = m2m_list

                # if (patient.category_ids != related_patient_rec.category_ids):

                m2m_list = []
                for category_id in related_patient_rec.category_ids:
                    m2m_list.append((3, category_id.id))
                for category_id in patient.category_ids:
                    m2m_list.append((4, category_id.id))
                if m2m_list != []:
                    vals['category_ids'] = m2m_list

                # if (patient.marker_ids.id is not False):

                m2m_list = []
                count = 0
                for global_tag_id in patient.marker_ids:
                    m2m_list.append((4, global_tag_id.id))
                    count += 1

                if count > 0:
                    vals['marker_ids'] = m2m_list

                if (patient.name != related_patient_rec.name):

                    vals['name'] = patient.name

                if (patient.code != related_patient_rec.code):

                    vals['code'] = patient.code

                if (patient.is_absent != related_patient_rec.is_absent):

                    vals['is_absent'] = patient.is_absent

                if (patient.gender != related_patient_rec.gender):

                    vals['gender'] = patient.gender

                if (patient.estimated_age != related_patient_rec.estimated_age):

                    vals['estimated_age'] = patient.estimated_age

                if (patient.birthday != related_patient_rec.birthday):

                    vals['birthday'] = patient.birthday

                if (patient.date_death != related_patient_rec.date_death):

                    vals['date_death'] = patient.date_death

                if (patient.force_is_deceased != related_patient_rec.force_is_deceased):

                    vals['force_is_deceased'] = patient.force_is_deceased

                if self.update_contact_info_data:

                    if (patient.contact_info_is_unavailable != related_patient_rec.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = patient.contact_info_is_unavailable

                    if (patient.validate_contact_information != related_patient_rec.validate_contact_information):

                        vals['validate_contact_information'] = patient.validate_contact_information

                    if (patient.zip != related_patient_rec.zip):

                        vals['zip'] = patient.zip

                    if (patient.street_name != related_patient_rec.street_name):

                        vals['street_name'] = patient.street_name

                    if (patient.street_number != related_patient_rec.street_number):

                        vals['street_number'] = patient.street_number

                    if (patient.street_number2 != related_patient_rec.street_number2):

                        vals['street_number2'] = patient.street_number2

                    if (patient.street2 != related_patient_rec.street2):

                        vals['street2'] = patient.street2

                    if (patient.country_id != related_patient_rec.country_id):

                        vals['country_id'] = patient.country_id.id

                    if (patient.state_id != related_patient_rec.state_id):

                        vals['state_id'] = patient.state_id.id

                    if (patient.city_id != related_patient_rec.city_id):

                        vals['city_id'] = patient.city_id.id

                    if (patient.phone is not False) and (patient.phone != related_patient_rec.phone):

                        vals['phone'] = patient.phone

                    if (patient.mobile is not False) and (patient.mobile != related_patient_rec.mobile):

                        vals['mobile'] = patient.mobile

                if vals != {}:

                    vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                related_patient_rec.write(vals)

            if self.related_patient_rec_verification_exec:
                if patient.related_patient_rec_id.id is not False:
                    patient.related_patient_rec_id._patient_rec_verification_exec()

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True
