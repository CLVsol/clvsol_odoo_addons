# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Residence (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Residence Module customizations for CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_base_jcafb',
        'clv_residence',
        'clv_document',
        'clv_lab_test',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/residence_seq.xml',
        'data/document.xml',
        'data/lab_test.xml',
        'data/set_element.xml',
        'views/residence_code_view.xml',
        'views/document_view.xml',
        'views/lab_test_view.xml',
        'wizard/residence_associate_to_set_view.xml',
        'wizard/residence_document_setup_view.xml',
        'wizard/residence_document_setup_2_view.xml',
        'wizard/residence_lab_test_result_setup_2_view.xml',
        'wizard/residence_set_code_view.xml',
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
