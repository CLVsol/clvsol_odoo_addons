# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Module',
    'summary': 'Base Module used by CLVsol Solutions.',
    'version': '16.0.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': ['base'],
    'data': [
        'security/base_security.xml',
        'security/ir.model.access.csv',
        'views/global_settings_view.xml',
        'views/global_settings_filestore_view.xml',
        'views/base_menu_view.xml',
        'views/global_settings_menu_view.xml',
        'views/health_menu_view.xml',
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
