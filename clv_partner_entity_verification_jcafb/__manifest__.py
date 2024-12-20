# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Entity Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Partner Entity Verification Module for CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_partner_entity',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_entity_street_pattern_view.xml',
        'views/partner_entity_street_pattern_match_view.xml',
        'views/partner_entity_contact_information_pattern_view.xml',
        'views/partner_entity_contact_information_pattern_match_view.xml',
        'views/referenceable_model_view.xml',
        'views/partner_entity_menu_view.xml',
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
