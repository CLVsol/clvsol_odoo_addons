# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Patient Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/street_pattern_match.xml',
        'data/contact_information_pattern_match.xml',
        'data/patient_verification.xml',
        'views/verification_outcome_view.xml',
        'wizard/patient_mass_edit_view.xml',
        'wizard/patient_verification_exec_view.xml',
        'wizard/patient_street_pattern_add_view.xml',
        'wizard/patient_contact_information_pattern_add_view.xml',
        'wizard/patient_related_residence_updt_view.xml',
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
