# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2017 Onestein (<http://www.onestein.eu>)
# Copyright (C) 2017-Today  Carlos Eduardo Vercelino - CLVsol
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
###############################################################################

{
    'name': 'Directory Files Download',
    'summary': 'Download all files of a directory on server',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Tools',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base_setup',
        'clv_base',
    ],
    'data': [
        'security/file_system_security.xml',
        'security/ir.model.access.csv',
        'views/filesystem_directory.xml',
        'views/file_system_directory_view.xml',
        'views/file_system_file_view.xml',
        'views/file_system_menu_view.xml',
        'wizard/file_system_directory_file_upload_view.xml',
    ],
    'installable': True,
}
