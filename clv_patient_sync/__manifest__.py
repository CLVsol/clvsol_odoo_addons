# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient External Sync',
    'summary': 'Patient External Sync Module used by CLVsol Solutions.',
    'version': '16.0.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient',
        'clv_external_sync',
    ],
    'data': [
        # 'data/patient_age_range.xml',
        'data/patient_age_range_sync.xml',
        'data/patient_category_sync.xml',
        'data/patient_marker_sync.xml',
        'data/patient_1_inc.xml',
        'data/patient_2_sync.xml',
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
