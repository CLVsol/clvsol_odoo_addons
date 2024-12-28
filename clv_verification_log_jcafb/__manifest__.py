# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Verification Log (for CLVhealth-JCAFB Solution)',
    'summary': 'Verification Log Module used in CLVhealth-JCAFB Solution.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_verification',
        'clv_global_log',
    ],
    'data': [
        'views/verification_outcome_log_view.xml',
        'views/verification_template_log_view.xml',
        'views/verification_schedule_log_view.xml',
        'views/verification_batch_log_view.xml',
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
