# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Lab Test Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Lab Test Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_lab_test_jcafb',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/lab_test_export_xls_param_verification.xml',
        'views/verification_outcome_view.xml',
        'wizard/lab_test_export_xls_param_verification_exec_view.xml',
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
