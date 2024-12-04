# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Event',
    'summary': 'Event Module used by CLVsol Solutions.',
    'version': '16.0.7.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_global_tag',
    ],
    'data': [
        'security/event_security.xml',
        'security/ir.model.access.csv',
        'views/event_view.xml',
        'views/event_category_view.xml',
        'views/global_tag_view.xml',
        'views/event_attendee_view.xml',
        'views/referenceable_model_view.xml',
        'views/phase_view.xml',
        'views/event_state_view.xml',
        'views/event_menu_view.xml',
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
