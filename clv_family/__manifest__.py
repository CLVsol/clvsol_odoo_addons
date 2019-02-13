# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Family',
    'summary': 'Family Module used by CLVsol Solutions.',
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
        'security/family_security.xml',
        'security/ir.model.access.csv',
        'views/family_view.xml',
        'views/family_log_view.xml',
        'views/family_category_view.xml',
        'views/family_category_log_view.xml',
        'views/res_partner_view.xml',
        'views/global_tag_view.xml',
        # 'views/family_name_view.xml',
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