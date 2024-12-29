# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Processing (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Processing Module customizations for CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_processing',
    ],
    'data': [
        'data/reregistration_import_xls.xml',
        'data/reregistration_import_xls_patient.xml',
        'data/patient_history_updt_from_person_history.xml',
        'data/residence_history_updt_from_address_history.xml',
        'data/copy_qsf_from_residence_to_patient.xml',
        'data/reregistration_import_xls_patient_2023.xml',
        'data/patient_estilmated_age_updt.xml',
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
