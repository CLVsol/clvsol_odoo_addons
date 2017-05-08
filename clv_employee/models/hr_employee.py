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

from odoo import api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    @api.depends('name', 'code', 'professional_id')
    def name_get(self):
        result = []
        for record in self:
            if record.professional_id is not False:
                if record.code is not False:
                    result.append(
                        (record.id,
                         u'%s [%s] (%s)' % (record.name, record.code, record.professional_id)
                         ))
                else:
                    result.append(
                        (record.id,
                         u'%s (%s)' % (record.name, record.professional_id)
                         ))
            else:
                if record.code is not False:
                    result.append(
                        (record.id,
                         u'%s [%s]' % (record.name, record.code)
                         ))
                else:
                    result.append(
                        (record.id,
                         u'%s' % (record.name)
                         ))
        return result

    code = fields.Char(string='Employee Code', required=False)

    professional_id = fields.Char(string='Professional ID', required=False)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),

        ('professional_id_uniq',
         'UNIQUE (professional_id)',
         u'Error! The Professional ID must be unique!'),
    ]
