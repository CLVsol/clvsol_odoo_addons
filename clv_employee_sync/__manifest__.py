# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Employee External Sync',
    'summary': 'Employee External Sync Module used by CLVsol Solutions.',
    'version': '16.0.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_employee',
        'clv_external_sync',
    ],
    'data': [
        'data/hr_department_1_rec.xml',
        'data/hr_department_2_sync.xml',
        'data/hr_job_sync.xml',
        'data/hr_employee_1_rec.xml',
        'data/hr_employee_2_sync.xml',
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
