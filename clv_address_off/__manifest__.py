# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Address (Off)',
    'summary': 'Address (Off) Module used by CLVsol Solutions.',
    'version': '4.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_base',
        'clv_global_log',
        'clv_partner_entity',
        'clv_global_tag',
    ],
    'data': [
        'security/address_off_security.xml',
        'security/ir.model.access.csv',
        'views/address_off_view.xml',
        'views/address_off_log_view.xml',
        'views/address_off_category_view.xml',
        'views/address_off_marker_view.xml',
        'views/res_partner_view.xml',
        'views/global_tag_view.xml',
        'views/address_off_name_view.xml',
        'views/address_view.xml',
        'wizard/address_off_mass_edit_view.xml',
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
