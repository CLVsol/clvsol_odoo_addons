# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.modules import get_module_resource
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PatientAux(models.Model):

    _name = 'clv.patient_aux'
    _description = 'Patient (Aux)'
    _inherit = 'clv.abstract.partner_entity'

    @api.depends('name', 'code', 'age_years')
    def name_get(self):
        result = []
        for record in self:
            if record.code and record.age_years:
                result.append(
                    (record.id,
                     u'%s [%s] (%s)' % (record.name, record.code, record.age_years)
                     ))
            else:
                if record.code:
                    result.append(
                        (record.id,
                         u'%s [%s]' % (record.name, record.code)
                         ))
                elif record.age_years:
                    result.append(
                        (record.id,
                         u'%s (%s)' % (record.name, record.age_years)
                         ))
                else:
                    result.append(
                        (record.id,
                         u'%s' % (record.name)
                         ))
        return result

    code = fields.Char(string='Patient (Aux) Code', required=False)

    notes = fields.Text(string='Notes:')

    estimated_age = fields.Char(string='Estimated Age', required=False)

    birthday = fields.Date(string="Date of Birth")
    age = fields.Char(
        string='Age',
        compute='_compute_age',
    )
    age_years = fields.Char(
        string="Age (years old)",
        compute='_compute_age',
    )

    @api.constrains('birthday')
    def _check_birthday(self):
        for patient_aux in self:
            if patient_aux.birthday:
                if patient_aux.birthday > fields.Date.today():
                    raise UserError(u'Date of Birth must be in the past!')

    def _compute_age(self):
        now = datetime.now()
        for r in self:
            if r.birthday:
                dob = datetime.strptime(str(r.birthday), '%Y-%m-%d')
                if r.is_deceased and bool(r.date_death):
                    dod = datetime.strptime(str(r.date_death), '%Y-%m-%d')
                    delta = relativedelta(dod, dob)
                    is_deceased = _(' (deceased)')
                elif r.is_deceased and not bool(r.date_death):
                    delta = relativedelta(now, dob)
                    is_deceased = _(' (deceased?)')
                else:
                    delta = relativedelta(now, dob)
                    is_deceased = ''
                years_months_days = '%d%s %d%s %d%s%s' % (
                    delta.years, _('y'), delta.months, _('m'), delta.days, _('d'),
                    is_deceased
                )
                years = '%d%s%s' % (
                    delta.years, _('y'),
                    is_deceased
                )
                r.age = years_months_days
                r.age_years = years
            else:
                r.age = "No Date of Birth!"
                r.age_years = False

    date_reference = fields.Date(
        string="Reference Date",
        compute='_compute_date_reference',
    )
    age_reference = fields.Char(
        string='Reference Age',
        compute='_compute_age_reference',
    )
    age_reference_years = fields.Char(
        string="Reference Age (years old)",
        compute='_compute_age_reference',
    )

    def _compute_date_reference(self):
        for r in self:
            date_reference = self.env['ir.config_parameter'].sudo().get_param(
                'clv.global_settings.current_date_reference', '').strip()
            r.date_reference = date_reference

    def _compute_age_reference(self):
        for r in self:
            if r.date_reference:
                dor = datetime.strptime(str(r.date_reference), '%Y-%m-%d')
                if r.birthday:
                    dob = datetime.strptime(str(r.birthday), '%Y-%m-%d')
                    if r.is_deceased and bool(r.date_death):
                        dod = datetime.strptime(str(r.date_death), '%Y-%m-%d')
                        delta = relativedelta(dod, dob)
                        is_deceased = _(' (deceased)')
                    elif r.is_deceased and not bool(r.date_death):
                        delta = relativedelta(dor, dob)
                        is_deceased = _(' (deceased?)')
                    else:
                        delta = relativedelta(dor, dob)
                        is_deceased = ''
                    years_months_days = '%d%s %d%s %d%s%s' % (
                        delta.years, _('y'), delta.months, _('m'), delta.days, _('d'),
                        is_deceased
                    )
                    years = '%d%s%s' % (
                        delta.years, _('y'),
                        is_deceased
                    )
                    r.age_reference = years_months_days
                    r.age_reference_years = years
                else:
                    r.age_reference = "No Date of Birth!"
                    r.age_reference_years = False
            else:
                r.age_reference = "No Date of Reference!"
                r.age_reference_years = False

    force_is_deceased = fields.Boolean(
        string='Force Is Deceased',
        default=False
    )
    date_death = fields.Date(
        string='Deceased Date',
    )
    is_deceased = fields.Boolean(
        string='Is Deceased',
        compute='_compute_is_deceased',
        search='_search_is_deceased'
    )

    def _compute_is_deceased(self):
        for record in self:
            if record.date_death:
                record.is_deceased = bool(record.date_death)
            record.is_deceased = bool(record.date_death) or record.force_is_deceased

    def _search_is_deceased(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return ['|', ('date_death', '!=', False), ('force_is_deceased', '=', True)]

    is_absent = fields.Boolean(
        string='Is Absent'
    )

    gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female'),
         ('O', 'Other'),
         ], string='Gender'
    )
    marital = fields.Selection(
        [('single', 'Single'),
         ('married', 'Married'),
         ('widower', 'Widower'),
         ('divorced', 'Divorced'),
         ('separated', 'Separated'),
         ('law marriage', 'law marriage'),
         ], string='Marital Status'
    )

    @api.model
    def _create_vals(self, vals):
        vals = super()._create_vals(vals)
        vals.update({
            'type': self._name,
        })
        return vals

    def _get_default_image_path(self, vals):
        res = super()._get_default_image_path(vals)
        if res:
            return res
        image_path = get_module_resource(
            'clv_patient_aux', 'static/src/img', 'patient_aux-avatar.png',
        )
        return image_path

    spouse_id = fields.Many2one(comodel_name='clv.patient', string='Spouse', ondelete='restrict')
    father_id = fields.Many2one(comodel_name='clv.patient', string='Father', ondelete='restrict')
    mother_id = fields.Many2one(comodel_name='clv.patient', string='Mother', ondelete='restrict')
    responsible_id = fields.Many2one(comodel_name='clv.patient', string='Responsible', ondelete='restrict')
    caregiver_id = fields.Many2one(comodel_name='clv.patient', string='Caregiver', ondelete='restrict')

    spouse_aux_id = fields.Many2one(comodel_name='clv.patient_aux', string='Spouse (Aux)', ondelete='restrict')
    father_aux_id = fields.Many2one(comodel_name='clv.patient_aux', string='Father (Aux)', ondelete='restrict')
    mother_aux_id = fields.Many2one(comodel_name='clv.patient_aux', string='Mother (Aux)', ondelete='restrict')
    responsible_aux_id = fields.Many2one(
        comodel_name='clv.patient_aux',
        string='Responsible (Aux)',
        ondelete='restrict'
    )
    caregiver_aux_id = fields.Many2one(comodel_name='clv.patient_aux', string='Caregiver (Aux)', ondelete='restrict')

    def write(self, values):
        ret = super().write(values)
        for record in self:
            if ('code' in values):
                if record.entity_code != values['code']:
                    vals = {}
                    vals['entity_code'] = values['code']
                    super().write(vals)
        return ret

    def do_patient_aux_clear_address_data(self):

        for patient_aux in self:

            data_values = {}

            data_values['street_name'] = False
            data_values['street_number'] = False
            data_values['street_number2'] = False
            data_values['street2'] = False
            data_values['zip'] = False
            data_values['city_id'] = False
            data_values['state_id'] = False
            data_values['country_id'] = False
            # data_values['phone'] = False
            # data_values['mobile'] = False

            _logger.info(u'>>>>>>>>>> %s', data_values)

            patient_aux.write(data_values)
