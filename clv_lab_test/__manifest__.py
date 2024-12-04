# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Lab Test',
    'summary': 'Lab Test Module used by CLVsol Solutions.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_phase',
    ],
    'data': [
        'security/lab_test_security.xml',
        'security/ir.model.access.csv',
        'views/lab_test_type_view.xml',
        'views/lab_test_type_parameter_view.xml',
        'views/lab_test_result_view.xml',
        'views/referenceable_model_view.xml',
        'views/lab_test_criterion_view.xml',
        'views/phase_view.xml',
        'views/lab_test_result_reg_state_view.xml',
        'views/lab_test_result_state_view.xml',
        'wizard/lab_test_result_mass_edit_view.xml',
        'wizard/lab_test_type_duplicate_view.xml',
        'wizard/lab_test_type_criteria_setup_view.xml',
        'wizard/lab_test_result_criteria_refresh_view.xml',
        'views/lab_test_menu_view.xml',
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
