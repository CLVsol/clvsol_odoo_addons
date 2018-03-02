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
    'name': 'Medicament',
    'summary': 'Medicament Module used by CLVsol Solutions.',
    'version': '3.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
    ],
    'data': [
        'security/medicament_security.xml',
        'security/ir.model.access.csv',
        'views/medicament_view.xml',
        'views/medicament_active_component_view.xml',
        'views/medicament_pres_form_view.xml',
        'views/medicament_uom_view.xml',
        'views/medicament_manufacturer_view.xml',
        'views/medicament_log_view.xml',
        'views/medicament_category_view.xml',
        'views/medicament_list_view.xml',
        'views/medicament_list_item_view.xml',
        'views/global_tag_view.xml',
        'wizard/medicament_updt_view.xml',
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
