# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Residence (Community)',
    'summary': 'Residence (Community) Module used by CLVsol Solutions.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_residence',
        'clv_address',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/address_view.xml',
        'wizard/address_mass_edit_view.xml',
        'wizard/address_associate_to_residence_view.xml',
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
