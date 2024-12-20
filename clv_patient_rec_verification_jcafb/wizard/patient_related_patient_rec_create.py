# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientRelatePatientRecCreate(models.TransientModel):
    _description = 'Patient Related Patient (Rec) Create'
    _name = 'clv.patient.related_patient_rec_create'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_related_patient_rec_create_rel',
        string='Patients',
        default=_default_patient_ids
    )

    related_patient_rec_verification_exec = fields.Boolean(
        string='Related Patient (Rec) Verification Execute',
        default=True,
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    def do_patient_related_patient_rec_create(self):
        self.ensure_one()

        PatientRec = self.env['clv.patient_rec']

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if not patient.related_patient_rec_is_unavailable:

                if patient.related_patient_rec_id.id is False:

                    # patient_rec = PatientRec.search([
                    #     ('name', '=', patient.name),
                    # ])
                    patient_rec = PatientRec.search([
                        ('code', '=', patient.code),
                    ])

                    if patient_rec.id is False:

                        vals = {}

                        if (patient.code is not False):

                            vals['code'] = patient.code

                        if (patient.phase_id.id is not False):

                            vals['phase_id'] = patient.phase_id.id

                        if (patient.state is not False):

                            vals['state'] = patient.state

                        if (patient.name is not False):

                            vals['name'] = patient.name

                        if (patient.is_absent is not False):

                            vals['is_absent'] = patient.is_absent

                        if (patient.gender is not False):

                            vals['gender'] = patient.gender

                        if (patient.estimated_age is not False):

                            vals['estimated_age'] = patient.estimated_age

                        if (patient.birthday is not False):

                            vals['birthday'] = patient.birthday

                        if (patient.date_death is not False):

                            vals['date_death'] = patient.date_death

                        if (patient.force_is_deceased is not False):

                            vals['force_is_deceased'] = patient.force_is_deceased

                        vals['contact_info_is_unavailable'] = patient.contact_info_is_unavailable

                        if (patient.zip is not False):

                            vals['zip'] = patient.zip

                        if (patient.street_name is not False):

                            vals['street_name'] = patient.street_name

                        if (patient.street_number is not False):

                            vals['street_number'] = patient.street_number

                        if (patient.street_number2 is not False):

                            vals['street_number2'] = patient.street_number2

                        if (patient.street2 is not False):

                            vals['street2'] = patient.street2

                        if (patient.country_id.id is not False):

                            vals['country_id'] = patient.country_id.id

                        if (patient.state_id.id is not False):

                            vals['state_id'] = patient.state_id.id

                        if (patient.city_id.id is not False):

                            vals['city_id'] = patient.city_id.id

                        if (patient.phone is not False):

                            vals['phone'] = patient.phone

                        if (patient.mobile is not False):

                            vals['mobile'] = patient.mobile

                        vals['validate_contact_information'] = patient.validate_contact_information

                        # if (patient.global_tag_ids.id is not False):

                        m2m_list = []
                        count = 0
                        for global_tag_id in patient.global_tag_ids:
                            m2m_list.append((4, global_tag_id.id))
                            count += 1

                        if count > 0:
                            vals['global_tag_ids'] = m2m_list

                        # if (patient.category_ids.id is not False):

                        m2m_list = []
                        count = 0
                        for category_id in patient.category_ids:
                            m2m_list.append((4, category_id.id))
                            count += 1

                        if count > 0:
                            vals['category_ids'] = m2m_list

                        # if (patient.marker_ids.id is not False):

                        m2m_list = []
                        count = 0
                        for marker_id in patient.marker_ids:
                            m2m_list.append((4, marker_id.id))
                            count += 1

                        if count > 0:
                            vals['marker_ids'] = m2m_list

                        if vals != {}:

                            vals['reg_state'] = 'revised'

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'vals:', vals)
                            new_related_patient_rec = PatientRec.create(vals)

                            values = {}
                            values['related_patient_rec_id'] = new_related_patient_rec.id
                            patient.write(values)

                    else:

                        values = {}
                        values['related_patient_rec_id'] = patient_rec.id
                        patient.write(values)

            if self.related_patient_rec_verification_exec:
                if patient.related_patient_rec_id.id is not False:
                    patient.related_patient_rec_id._patient_rec_verification_exec()

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True
