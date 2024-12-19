# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResidenceCodePoolSeek(models.TransientModel):
    _description = 'Residence Code Pool Seek'
    _name = 'clv.residence.code_pool.item_seek'

    def _default_residence_code_pool_ids(self):
        return self._context.get('active_ids')
    residence_code_pool_ids = fields.Many2many(
        comodel_name='clv.residence.code_pool',
        relation='clv_residence_code_pool_residence_code_pool_item_seek_rel',
        string='Residence Code Pools',
        default=_default_residence_code_pool_ids
    )

    def do_residence_code_pool_item_seek(self):
        self.ensure_one()

        ResidenceCodePoolItem = self.env['clv.residence.code_pool.item']
        Residence = self.env['clv.residence']

        for residence_code_pool in self.residence_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', residence_code_pool.name)

            search_domain = [
                ('residence_code_pool_id', '=', residence_code_pool.id),
            ]
            items = ResidenceCodePoolItem.search(search_domain)

            for item in items:

                if (item.residence_id is not False):

                    item.residence_id = False

            for item in items:

                residences = Residence.search([])

                for residence in residences:

                    if (residence.code == item.code):

                        item.residence_id = residence.id

        return True
