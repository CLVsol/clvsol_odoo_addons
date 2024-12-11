# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Lab Test Survey Association (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Lab Test Survey Association Module used by CLVsol Solutions.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_lab_test',
        'clv_survey',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_view.xml',
        'views/lab_test_type_view.xml',
        'data/survey_survey.xml',
        'data/survey_user_input.xml',
        'wizard/lab_test_result_criteria_updt_from_survey_view.xml',
        'wizard/lab_test_result_set_survey_user_input_view.xml',
        'wizard/lab_test_result_survey_user_input_refresh_view.xml',
        'wizard/lab_test_result_survey_user_input_set_in_progress_view.xml',
        'wizard/lab_test_result_survey_user_input_validate_view.xml',
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
