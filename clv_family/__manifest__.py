# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Family',
    'summary': 'Family Module used by CLVsol Solutions.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_base',
        'clv_partner_entity',
        'clv_global_log',
        'clv_global_tag',
        'clv_address',
        'clv_employee',
    ],
    'data': [
        'security/family_security.xml',
        'security/ir.model.access.csv',
        'data/global_settings.xml',
        'data/default_value.xml',
        'views/family_view.xml',
        'views/family_log_view.xml',
        'views/family_category_view.xml',
        'views/family_category_log_view.xml',
        'views/family_marker_view.xml',
        'views/family_tag_view.xml',
        'views/res_partner_view.xml',
        'views/global_tag_view.xml',
        'views/family_name_view.xml',
        'views/global_settings_view.xml',
        'views/address_view.xml',
        'views/phase_view.xml',
        'views/family_reg_state_view.xml',
        'views/family_state_view.xml',
        'views/employee_view.xml',
        'wizard/family_mass_edit_view.xml',
        'wizard/family_contact_information_updt_view.xml',
        'views/family_menu_view.xml',
        'data/global_log_client.xml',
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
