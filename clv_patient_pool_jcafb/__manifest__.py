# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient Code Pool (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Patient Code Pool Module customizations for CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient_jcafb',
        'clv_pool',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_code_pool_view.xml',
        'views/patient_code_pool_item_view.xml',
        'views/pool_menu_view.xml',
        'wizard/patient_code_pool_item_setup_view.xml',
        'wizard/patient_code_pool_item_seek_view.xml',
        'wizard/patient_code_pool_item_mass_edit_view.xml',
        'wizard/patient_code_pool_item_get_view.xml',
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
