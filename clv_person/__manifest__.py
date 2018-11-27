# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Person',
    'summary': 'Person Module used by CLVsol Solutions.',
    'version': '4.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_global_log',
        'clv_entity',
        'clv_global_tag',
    ],
    'data': [
        'security/person_security.xml',
        'security/ir.model.access.csv',
        'views/person_view.xml',
        'views/person_log_view.xml',
        'views/person_marker_view.xml',
        'views/person_category_view.xml',
        'views/person_category_log_view.xml',
        'views/res_partner_view.xml',
        'views/global_tag_view.xml',
        'wizard/person_mass_edit_view.xml',
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
