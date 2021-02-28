# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'clv.patient'

    patient_aux_ids = fields.One2many(
        comodel_name='clv.patient_aux',
        inverse_name='related_patient_id',
        string='Patients (Aux)'
    )
    count_patients_aux = fields.Integer(
        string='Patients (Aux) (count)',
        compute='_compute_count_patients_aux',
    )

    @api.depends('patient_aux_ids')
    def _compute_count_patients_aux(self):
        for r in self:
            r.count_patients_aux = len(r.patient_aux_ids)


class PatientAux(models.Model):
    _inherit = 'clv.patient_aux'

    related_patient_is_unavailable = fields.Boolean(
        string='Related Patient is unavailable',
        default=False,
    )
    related_address_id = fields.Many2one(comodel_name='clv.address', string='Related Address', ondelete='restrict')
    related_patient_id = fields.Many2one(comodel_name='clv.patient', string='Related Patient', ondelete='restrict')
    related_patient_name = fields.Char(string='Related Patient Name', related='related_patient_id.name')
    related_patient_code = fields.Char(string='Related Patient Code', related='related_patient_id.code')
    related_patient_category_ids = fields.Many2many(
        comodel_name='clv.patient.category',
        string='Related Patient Categories',
        related='related_patient_id.category_ids'
    )

    def do_patient_aux_get_related_patient_data(self):

        for patient_aux in self:

            _logger.info(u'>>>>> %s', patient_aux.related_patient_id)

            if (patient_aux.reg_state in ['draft', 'revised']) and \
               (patient_aux.related_patient_id.id is not False):

                data_values = {}
                data_values['name'] = patient_aux.related_patient_id.name
                data_values['code'] = patient_aux.related_patient_id.code
                data_values['is_absent'] = patient_aux.related_patient_id.is_absent
                data_values['gender'] = patient_aux.related_patient_id.gender
                data_values['birthday'] = patient_aux.related_patient_id.birthday
                data_values['date_death'] = patient_aux.related_patient_id.date_death
                data_values['force_is_deceased'] = patient_aux.related_patient_id.force_is_deceased

                data_values['contact_info_is_unavailable'] = patient_aux.related_patient_id.contact_info_is_unavailable

                data_values['street_name'] = patient_aux.related_patient_id.street_name
                data_values['street_number'] = patient_aux.related_patient_id.street_number
                data_values['street_number2'] = patient_aux.related_patient_id.street_number2
                data_values['street2'] = patient_aux.related_patient_id.street2
                data_values['zip'] = patient_aux.related_patient_id.zip
                data_values['city'] = patient_aux.related_patient_id.city
                data_values['city_id'] = patient_aux.related_patient_id.city_id.id
                data_values['state_id'] = patient_aux.related_patient_id.state_id.id
                data_values['country_id'] = patient_aux.related_patient_id.country_id.id
                data_values['phone'] = patient_aux.related_patient_id.phone
                data_values['mobile'] = patient_aux.related_patient_id.mobile

                data_values['state'] = patient_aux.related_patient_id.state

                PatientCategory = self.env['clv.patient.category']
                m2m_list = []
                for patient_category_id in patient_aux.related_patient_id.category_ids:
                    patient_category = PatientCategory.search([
                        ('name', '=', patient_category_id.name),
                    ])
                    m2m_list.append((4, patient_category.id))
                data_values['category_ids'] = m2m_list

                _logger.info(u'>>>>>>>>>> %s', data_values)

                patient_aux.write(data_values)

        return True


class PatientAux_2(models.Model):
    _inherit = 'clv.patient_aux'

    related_patient_state = fields.Selection(
        string='Related Patient State',
        related='related_patient_id.state',
        store=False
    )
