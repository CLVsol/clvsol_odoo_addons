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

{
    'name': 'Person',
    'summary': 'Person Module used by CLVsol Solutions.',
    'version': '3.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_address',
        'clv_data_export',
    ],
    'data': [
        'security/person_security.xml',
        'security/ir.model.access.csv',
        'views/person_view.xml',
        'views/person_category_view.xml',
        'views/person_log_view.xml',
        'views/address_view.xml',
        'views/person_address_role_view.xml',
        'views/global_tag_view.xml',
        'views/person_annotation_view.xml',
        'views/person_annotation_log_view.xml',
        'views/data_export_view.xml',
        'wizard/person_updt_view.xml',
        'wizard/person_address_updt_view.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
