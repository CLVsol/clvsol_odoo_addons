# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResidenceCodePoolGet(models.TransientModel):
    _description = 'Residence Code Pool Get'
    _name = 'clv.residence.code_pool.item_get'

    def _default_residence_code_pool_ids(self):
        return self._context.get('active_ids')
    residence_code_pool_ids = fields.Many2many(
        comodel_name='clv.residence.code_pool',
        relation='clv_residence_code_pool_residence_code_pool_item_get_rel',
        string='Residence Code Pools',
        default=_default_residence_code_pool_ids
    )

    def do_residence_code_pool_item_get(self):
        self.ensure_one()

        ResidenceCodePoolItem = self.env['clv.residence.code_pool.item']
        Residence = self.env['clv.residence']

        for residence_code_pool in self.residence_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', residence_code_pool.name)

            residences = Residence.search([])
            items = ResidenceCodePoolItem.search([])

            for residence in residences:

                found_item = False
                for item in items:

                    if (residence.code == item.code):
                        found_item = True

                if not found_item:

                    if residence.code is not False:

                        sequence_str = residence.code[:7].replace('.', '')
                        format_code = self.env['clv.abstract.code'].format_code(sequence_str)

                        if residence.code == format_code:

                            values = {
                                'residence_code_pool_id': residence_code_pool.id,
                                'code_sequence': residence_code_pool.code_sequence,
                                'code': residence.code,
                                'residence_id': residence.id,
                                'notes': 'New'
                            }

                        else:

                            values = {
                                'residence_code_pool_id': residence_code_pool.id,
                                'code_sequence': residence_code_pool.code_sequence,
                                'code': residence.code,
                                'residence_id': residence.id,
                                'notes': 'New (Invalid)'
                            }

                        residence_code_pool_item = ResidenceCodePoolItem.create(values)

                        _logger.info(u'%s %s - %s', '>>>>>>>>>>', residence_code_pool_item.code, residence_code_pool_item.notes)

        return True
