# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient (Rec) Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Patient (Rec) Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient_rec',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_rec_verification.xml',
        'data/patient_verification.xml',
        # 'data/default_value.xml',
        'data/street_pattern_match.xml',
        'data/contact_information_pattern_match.xml',
        'views/verification_outcome_view.xml',
        'wizard/patient_rec_mass_edit_view.xml',
        'wizard/patient_rec_verification_exec_view.xml',
        'wizard/patient_related_patient_rec_updt_view.xml',
        'wizard/patient_related_patient_rec_create_view.xml',
        'wizard/patient_reload_view.xml',
        'wizard/patient_rec_street_pattern_add_view.xml',
        'wizard/patient_rec_contact_information_pattern_add_view.xml',
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
