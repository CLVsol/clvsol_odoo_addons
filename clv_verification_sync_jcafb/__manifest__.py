# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Verification External Sync (for CLVhealth-JCAFB Solution)',
    'summary': 'Verification External Sync Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_verification_jcafb',
        'clv_external_sync',
    ],
    'data': [
        'data/partner_entity_street_pattern_sync.xml',
        'data/partner_entity_contact_information_pattern_sync.xml',
        'data/verification_marker_sync.xml',
        'data/verification_outcome_1_sync.xml',
        'data/verification_outcome_2_sync.xml',
        'data/verification_outcome_3_sync.xml',
        'data/verification_outcome_4_sync.xml',
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
