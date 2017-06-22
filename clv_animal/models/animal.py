# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.fields import Date as fDate
from odoo.exceptions import UserError


class Animal(models.Model):
    _description = 'Animal'
    _name = 'clv.animal'
    _order = 'name'

    @api.multi
    @api.depends('name', 'code', 'age')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s] (%s)' % (record.name, record.code, record.age)
                 ))
        return result

    name = fields.Char(string='Name', required=True)

    code = fields.Char(string='Animal Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string="Inclusion Date", required=False, readonly=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    country_id = fields.Many2one(comodel_name='res.country', string='Nationality')
    birthday = fields.Date(string="Date of Birth")
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True
    )
    estimated_age = fields.Char(string='Estimated Age', required=False)
    date_reference = fields.Date(string="Reference Date")
    age_reference = fields.Char(
        string='Reference Age',
        compute='_compute_age_reference',
        store=True
    )

    father_id = fields.Many2one(comodel_name='clv.animal', string='Father', ondelete='restrict')
    mother_id = fields.Many2one(comodel_name='clv.animal', string='Mother', ondelete='restrict')
    tutor_id = fields.Many2one(comodel_name='clv.person', string='Tutor', ondelete='restrict')

    identification_id = fields.Char(string='Animal ID')
    gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female')
         ], 'Gender'
    )
    spayed = fields.Selection(
        [('Y', 'Yes'),
         ('N', 'No')
         ], 'Spayed'
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Animal Code must be unique!'
         )
    ]

    @api.multi
    @api.constrains('birthday')
    def _check_birthday(self):
        for animal in self:
            if animal.birthday > fields.Date.today():
                raise UserError(u'Date of Birth must be in the past!')

    @api.one
    @api.depends('birthday')
    def _compute_age(self):
        now = datetime.now()
        if self.birthday:
            dob = datetime.strptime(self.birthday, '%Y-%m-%d')
            delta = relativedelta(now, dob)
            # self.age = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
            self.age = str(delta.years)
        else:
            self.age = "No Date of Birth!"

    @api.one
    @api.depends('date_reference', 'birthday')
    def _compute_age_reference(self):
        if self.date_reference:
            if self.birthday:
                dob = datetime.strptime(self.birthday, '%Y-%m-%d')
                now = datetime.strptime(self.date_reference, '%Y-%m-%d')
                delta = relativedelta(now, dob)
                # self.age_reference = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
                self.age_reference = str(delta.years)
            else:
                self.age_reference = "No Date of Birth!"
        else:
            self.age_reference = "No Reference Date!"

    @api.multi
    @api.depends('birthday')
    def _compute_age_days(self):
        today = fDate.from_string(fDate.today())
        for animal in self.filtered('birthday'):
            delta = (today - fDate.from_string(animal.birthday))
            animal.age_days = delta.days
