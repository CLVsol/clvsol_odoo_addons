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

from odoo import fields, models


class EmployeeMng(models.Model):
    _description = 'Employee Management'
    _name = 'clv.employee.mng'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

    history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='History Marker',
        ondelete='restrict'
    )

    code = fields.Char(string='Employee Code', required=False)
    professional_id = fields.Char(string='Professional ID', required=False)

    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')

    department_id = fields.Many2one('hr.department', string='Department')
    job_id = fields.Many2one('hr.job', string='Job Title')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    partner_id = fields.Many2one(comodel_name='res.partner', string='Related Partner', ondelete='restrict')
    user_id = fields.Many2one(comodel_name='res.users', string='Related User', ondelete='restrict')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Related Employee', ondelete='restrict')

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),

        ('professional_id_uniq',
         'UNIQUE (professional_id)',
         u'Error! The Professional ID must be unique!'),
    ]
