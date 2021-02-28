# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Person(models.Model):
    _inherit = 'clv.person'

    is_patient = fields.Boolean(
        string='Is Patient',
        default=False
    )

    patient_ids = fields.One2many(
        comodel_name='clv.patient',
        inverse_name='related_person_id',
        string='Patients'
    )
    count_patients = fields.Integer(
        string='Patients (count)',
        compute='_compute_count_patients',
        store=False
    )

    @api.depends('patient_ids')
    def _compute_count_patients(self):
        for r in self:
            r.count_patients = len(r.patient_ids)


class Patient(models.Model):
    _inherit = 'clv.patient'

    related_person_is_unavailable = fields.Boolean(
        string='Related Person is unavailable',
        default=True,
    )

    related_person_id = fields.Many2one(comodel_name='clv.person', string='Related Person', ondelete='restrict')
    related_person_name = fields.Char(string='Related Person Name', related='related_person_id.name')
    related_person_code = fields.Char(string='Related Person Code', related='related_person_id.code')
    related_person_category_ids = fields.Many2many(
        comodel_name='clv.person.category',
        string='Related Person Categories',
        related='related_person_id.category_ids'
    )
    related_person_state = fields.Selection(
        string='Related Person State',
        related='related_person_id.state',
        store=False
    )
    related_person_ref_address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Related Person Address',
        related='related_person_id.ref_address_id'
    )
    related_person_ref_address_code = fields.Char(
        string='Related Person Address Code',
        related='related_person_id.ref_address_id.code'
    )
    related_person_ref_address_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        string='Related Person Address Categories',
        related='related_person_id.ref_address_id.category_ids'
    )

    def do_patient_get_related_person_data(self):

        for patient in self:

            _logger.info(u'>>>>> %s', patient.related_person_id)

            if (patient.reg_state in ['draft', 'revised']) and \
               (patient.related_person_id.id is not False):

                data_values = {}
                data_values['name'] = patient.related_person_id.name
                data_values['code'] = patient.related_person_id.code
                data_values['is_absent'] = patient.related_person_id.is_absent
                data_values['gender'] = patient.related_person_id.gender
                data_values['birthday'] = patient.related_person_id.birthday
                data_values['date_death'] = patient.related_person_id.date_death
                data_values['force_is_deceased'] = patient.related_person_id.force_is_deceased

                data_values['contact_info_is_unavailable'] = patient.related_person_id.contact_info_is_unavailable

                data_values['street_name'] = patient.related_person_id.street_name
                data_values['street_number'] = patient.related_person_id.street_number
                data_values['street_number2'] = patient.related_person_id.street_number2
                data_values['street2'] = patient.related_person_id.street2
                data_values['zip'] = patient.related_person_id.zip
                data_values['city'] = patient.related_person_id.city
                data_values['city_id'] = patient.related_person_id.city_id.id
                data_values['state_id'] = patient.related_person_id.state_id.id
                data_values['country_id'] = patient.related_person_id.country_id.id
                data_values['phone'] = patient.related_person_id.phone
                data_values['mobile'] = patient.related_person_id.mobile

                data_values['state'] = patient.related_person_id.state

                data_values['phase_id'] = patient.related_person_id.phase_id.id
                data_values['random_field'] = patient.related_person_id.random_field

                PatientCategory = self.env['clv.patient.category']
                m2m_list = []
                for person_category_id in patient.related_person_id.category_ids:
                    patient_category = PatientCategory.search([
                        ('name', '=', person_category_id.name),
                    ])
                    m2m_list.append((4, patient_category.id))
                data_values['category_ids'] = m2m_list

                data_values['employee_id'] = patient.related_person_id.employee_id.id

                _logger.info(u'>>>>>>>>>> %s', data_values)

                patient.write(data_values)

        return True
