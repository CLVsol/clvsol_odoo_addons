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

from openerp import fields, models


class MedicamentDispensationExport(models.Model):
    _description = 'Medicament Dispensation Export'
    _name = 'clv.medicament.dispensation.export'
    _inherit = 'clv.object.export', 'clv.code.model'

    code = fields.Char(string='Medicament Dispensation Export Code', required=False, default='/')
    code_sequence = fields.Char(default='clv.export.code')

    date_start = fields.Date(
        string="Start Date", required=True, readonly=False,
    )
    date_end = fields.Date(
        string="End Date", required=True, readonly=False,
    )
    file_name_template = fields.Char(
        string='File Name', required=True,
        default='bb_dispensation_<date_start>_a_<date_end>')

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]
