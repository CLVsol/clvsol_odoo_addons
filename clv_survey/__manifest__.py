# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Survey',
    'summary': 'Survey Module used by CLVsol Solutions.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'survey',
        'clv_base',
        'clv_phase',
        'clv_set',
    ],
    'data': [
        'security/survey_security.xml',
        'security/ir.model.access.csv',
        'views/survey_survey_view.xml',
        'views/survey_question_view.xml',
        'views/survey_question_answer_view.xml',
        'views/survey_user_input_view.xml',
        'views/phase_view.xml',
        'views/referenceable_model_view.xml',
        # 'wizard/survey_duplicate_view.xml',
        'wizard/survey_code_renew_view.xml',
        # 'wizard/survey_export_xls_view.xml',
        # 'wizard/survey_export_xml_view.xml',
        'wizard/question_duplicate_view.xml',
        # 'wizard/question_label_setup_view.xml',
        'wizard/survey_user_input_mass_edit_view.xml',
        'wizard/survey_user_input_get_reference_view.xml',
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
