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
    'name': 'Person Off (for CLVhealth-JCAFB Solution)',
    'summary': 'Person Off Module for CLVhealth-JCAFB Solution.',
    'version': '3.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_off',
        'clv_address',
        'clv_person',
    ],
    'data': [
        'security/person_off_security.xml',
        'security/ir.model.access.csv',
        'views/person_off_view.xml',
        'views/address_name_view.xml',
        'views/off_instance_view.xml',
        'views/global_tag_view.xml',
        'views/person_off_log_view.xml',
        'wizard/person_off_updt_view.xml',
        'wizard/person_off_related_address_confirm_view.xml',
        'wizard/person_off_address_confirm_view.xml',
        'wizard/person_off_person_confirm_view.xml',
        'wizard/person_off_person_update_view.xml',
        'wizard/person_off_address_search_view.xml',
        'wizard/person_off_address_create_view.xml',
        'wizard/person_off_person_search_view.xml',
        'wizard/person_off_person_create_view.xml',
        'wizard/person_off_update_data_view.xml',
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
