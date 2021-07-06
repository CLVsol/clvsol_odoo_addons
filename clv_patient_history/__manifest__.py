# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient History',
    'summary': 'Patient History Module used in CLVsol Solutions.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient',
        'clv_phase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_history_view.xml',
        'views/phase_view.xml',
        'views/patient_view.xml',
        'views/residence_view.xml',
        'views/patient_history_reg_state_view.xml',
        'views/patient_history_state_view.xml',
        'views/employee_view.xml',
        'wizard/patient_history_updt_view.xml',
        'wizard/patient_history_patient_associate_to_set_view.xml',
        'wizard/patient_history_patient_mass_edit_view.xml',
        'views/patient_history_menu_view.xml',
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
