# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PatientRec(models.Model):
    _inherit = 'clv.patient_rec'

    patient_ids = fields.One2many(
        comodel_name='clv.patient',
        inverse_name='related_patient_rec_id',
        string='Patients'
    )
    count_patients = fields.Integer(
        string='Patients (count)',
        compute='_compute_count_patients',
    )

    @api.depends('patient_ids')
    def _compute_count_patients(self):
        for r in self:
            r.count_patients = len(r.patient_ids)


class Patient(models.Model):
    _inherit = 'clv.patient'

    related_patient_rec_is_unavailable = fields.Boolean(
        string='Related Patient (Rec) is unavailable',
        default=False,
    )
    # related_address_id = fields.Many2one(comodel_name='clv.address', string='Related Address', ondelete='restrict')
    related_patient_rec_id = fields.Many2one(comodel_name='clv.patient_rec', string='Related Patient (Rec)', ondelete='restrict')
    related_patient_rec_name = fields.Char(string='Related Patient (Rec) Name', related='related_patient_rec_id.name')
    related_patient_rec_code = fields.Char(string='Related Patient (Rec) Code', related='related_patient_rec_id.code')
    related_patient_rec_category_ids = fields.Many2many(
        comodel_name='clv.patient.category',
        string='Related Patient (Rec) Categories',
        related='related_patient_rec_id.category_ids'
    )

    def do_patient_get_related_patient_rec_data(self):

        for patient in self:

            _logger.info(u'>>>>> %s', patient.related_patient_rec_id)

            if (patient.reg_state in ['draft', 'revised']) and \
               (patient.related_patient_rec_id.id is not False):

                data_values = {}
                data_values['name'] = patient.related_patient_rec_id.name
                data_values['code'] = patient.related_patient_rec_id.code
                data_values['is_absent'] = patient.related_patient_rec_id.is_absent
                data_values['gender'] = patient.related_patient_rec_id.gender
                data_values['birthday'] = patient.related_patient_rec_id.birthday
                data_values['date_death'] = patient.related_patient_rec_id.date_death
                data_values['force_is_deceased'] = patient.related_patient_rec_id.force_is_deceased

                data_values['contact_info_is_unavailable'] = patient.related_patient_rec_id.contact_info_is_unavailable

                data_values['street_name'] = patient.related_patient_rec_id.street_name
                data_values['street_number'] = patient.related_patient_rec_id.street_number
                data_values['street_number2'] = patient.related_patient_rec_id.street_number2
                data_values['street2'] = patient.related_patient_rec_id.street2
                data_values['zip'] = patient.related_patient_rec_id.zip
                data_values['city'] = patient.related_patient_rec_id.city
                data_values['city_id'] = patient.related_patient_rec_id.city_id.id
                data_values['state_id'] = patient.related_patient_rec_id.state_id.id
                data_values['country_id'] = patient.related_patient_rec_id.country_id.id
                data_values['phone'] = patient.related_patient_rec_id.phone
                data_values['mobile'] = patient.related_patient_rec_id.mobile

                data_values['state'] = patient.related_patient_rec_id.state

                PatientCategory = self.env['clv.patient.category']
                m2m_list = []
                for patient_category_id in patient.related_patient_rec_id.category_ids:
                    patient_category = PatientCategory.search([
                        ('name', '=', patient_category_id.name),
                    ])
                    m2m_list.append((4, patient_category.id))
                data_values['category_ids'] = m2m_list

                _logger.info(u'>>>>>>>>>> %s', data_values)

                patient.write(data_values)

        return True


class Patient_2(models.Model):
    _inherit = 'clv.patient'

    related_patient_rec_state = fields.Selection(
        string='Related Patient (Rec) State',
        related='related_patient_rec_id.state',
        store=False
    )
