# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Employee Summary (for CLVhealth-JCAFB Solution)',
    'summary': 'Employee Summary Module used in CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_employee_jcafb',
        'clv_summary_jcafb',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/employee_summary.xml',
        'views/summary_view.xml',
        'wizard/employee_summary_setup_view.xml',
        'wizard/hr_employee_mass_edit_view.xml',
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
