# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging

from odoo import api, fields, models, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    disable_web_access = fields.Boolean(
        string='Disable Web Access', help="Check to disable user web access.",
        default=False
    )

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        """Verifies and returns the user ID corresponding to the given
          ``login`` and ``password`` combination, or False if there was
          no matching user.
           :param str db: the database on which user is trying to authenticate
           :param str login: username
           :param str password: user password
           :param dict user_agent_env: environment dictionary describing any
               relevant environment attributes
        """
        uid = cls._login(db, login, password)

        cr = cls.pool.cursor()
        try:
            cr.execute('SELECT disable_web_access FROM res_users WHERE id=%s', (uid,))
            if cr.rowcount:
                disable_web_access = cr.fetchone()[0]
                if disable_web_access is True:
                    _logger.warning("Web Access is disable for login '" + login + "'.")
                    return 0
        except Exception:
            _logger.exception("Failed to verify disable_web_access configuration parameter")
        finally:
            cr.close()

        if uid == SUPERUSER_ID:
            # Successfully logged in as admin!
            # Attempt to guess the web base url...
            if user_agent_env and user_agent_env.get('base_location'):
                try:
                    with cls.pool.cursor() as cr:
                        base = user_agent_env['base_location']
                        ICP = api.Environment(cr, uid, {})['ir.config_parameter']
                        if not ICP.get_param('web.base.url.freeze'):
                            ICP.set_param('web.base.url', base)
                except Exception:
                    _logger.exception("Failed to update web.base.url configuration parameter")
        return uid
