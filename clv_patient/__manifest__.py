# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient',
    'summary': 'Patient Module used by CLVsol Solutions.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_partner_entity',
        'clv_global_log',
        'clv_global_tag',
        'clv_employee',
        'clv_set',
        'clv_residence',
    ],
    'data': [
        'security/patient_security.xml',
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/patient_log_view.xml',
        'views/patient_category_view.xml',
        'views/patient_category_log_view.xml',
        'views/patient_marker_view.xml',
        'views/patient_tag_view.xml',
        'views/res_partner_view.xml',
        'views/global_tag_view.xml',
        'views/address_name_view.xml',
        'views/global_settings_view.xml',
        'views/phase_view.xml',
        'views/patient_reg_state_view.xml',
        'views/patient_state_view.xml',
        'views/employee_view.xml',
        'views/random_view.xml',
        'views/set_element_view.xml',
        'views/patient_age_range_view.xml',
        'views/residence_view.xml',
        'wizard/patient_mass_edit_view.xml',
        'views/patient_menu_view.xml',
        'data/global_log_client.xml',
        "data/patient_compute_age_reference_cron.xml",
        "data/patient_update_age_range_id_cron.xml",
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
