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
from odoo.exceptions import UserError


class PersonOff(models.Model):
    _description = 'Person Off'
    _name = 'clv.person.off'
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

    code = fields.Char(string='Person Code', required=False)

    notes = fields.Text(string='Notes')

    gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female')
         ], string='Gender'
    )

    birthday = fields.Date(string="Date of Birth")
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True
    )
    estimated_age = fields.Char(string='Estimated Age', required=False)

    responsible_name = fields.Char(string='Responsible Name', required=False)
    responsible_id = fields.Many2one(comodel_name='clv.person', string='Responsible', ondelete='restrict')
    caregiver_name = fields.Char(string='Caregiver Name', required=False)
    caregiver_id = fields.Many2one(comodel_name='clv.person', string='Caregiver', ondelete='restrict')

    active = fields.Boolean(string='Active', default=1)

    @api.multi
    @api.constrains('birthday')
    def _check_birthday(self):
        for person in self:
            if person.birthday > fields.Date.today():
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

    person_id = fields.Many2one(comodel_name='clv.person', string='Related Person', ondelete='restrict')
    person_gender = fields.Selection(string='Person Gender', related='person_id.gender')
    person_birthday = fields.Date(string='Person Date of Birth', related='person_id.birthday')
    person_responsible_id = fields.Many2one(
        comodel_name='clv.person',
        string='Person Responsible',
        related='person_id.responsible_id'
    )
    person_caregiver_id = fields.Many2one(
        comodel_name='clv.person',
        string='Person Caregiver',
        related='person_id.caregiver_id'
    )
    person_category_ids = fields.Char(
        string='Person Categories',
        related='person_id.category_ids.name',
        store=True
    )
    person_phone = fields.Char(string='Person Phone', related='person_id.phone')
    person_mobile = fields.Char(string='Person Mobile', related='person_id.mobile')
    person_history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='Person History Marker',
        related='person_id.history_marker_id'
    )
    person_address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Person Address',
        related='person_id.address_id'
    )

    address_name = fields.Char(string='Address Name', required=False, index=True)

    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    zip = fields.Char(string='ZIP code', change_default=True)
    city = fields.Char(string='City')
    state_id = fields.Many2one(comodel_name="res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one(comodel_name='res.country', string='Country', ondelete='restrict')

    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')

    addr_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        relation='clv_person_off_addr_category_rel',
        column1='addr_id',
        column2='category_id',
        string='Address Categories'
    )
    addr_category_names = fields.Char(
        string='Address Category Names',
        compute='_compute_addr_category_names',
        store=True
    )
    addr_category_names_suport = fields.Char(
        string='Address Category Names Suport',
        compute='_compute_addr_category_names_suport',
        store=False
    )

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}

    @api.depends('addr_category_ids')
    def _compute_addr_category_names(self):
        for r in self:
            r.addr_category_names = r.addr_category_names_suport

    @api.multi
    def _compute_addr_category_names_suport(self):
        for r in self:
            addr_category_names = False
            for category in r.addr_category_ids:
                if addr_category_names is False:
                    addr_category_names = category.complete_name
                else:
                    addr_category_names = addr_category_names + ', ' + category.addr_complete_name
            r.addr_category_names_suport = addr_category_names
            if r.addr_category_names != addr_category_names:
                record = self.env['clv.person.off'].search([('id', '=', r.id)])
                record.write({'addr_category_ids': r.addr_category_ids})

    address_id = fields.Many2one(comodel_name='clv.address', string='Related Address', ondelete='restrict')
    address_code = fields.Char(string='Address Code', related='address_id.code', store=False)

    address_phone = fields.Char(string='Address Phone', related='address_id.phone')
    address_mobile_phone = fields.Char(string='Address Mobile', related='address_id.mobile')

    address_category_ids = fields.Char(
        string='Address Categories',
        related='address_id.category_ids.name',
        store=True
    )
    address_history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='Address History Marker',
        related='address_id.history_marker_id'
    )

    action_person = fields.Selection(
        [('undefined', 'Undefined'),
         ('confirm', 'Confirm'),
         ('update', 'Update'),
         ('create', 'Create'),
         ('remove', 'Remove'),
         ('none', 'None'),
         ], string='Action (Person)', default='undefined'
    )

    action_address = fields.Selection(
        [('undefined', 'Undefined'),
         ('confirm', 'Confirm'),
         ('update', 'Update'),
         ('create', 'Create'),
         ('remove', 'Remove'),
         ('none', 'None'),
         ], string='Action (Address)', default='undefined'
    )

    action_person_address = fields.Selection(
        [('undefined', 'Undefined'),
         ('confirm', 'Confirm'),
         ('move', 'Move'),
         ('remove', 'Remove'),
         ('none', 'None'),
         ], string='Action (Person Address)', default='undefined'
    )

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]
