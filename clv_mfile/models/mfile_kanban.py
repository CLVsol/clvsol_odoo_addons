# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import api, fields, models
# from odoo import tools
from odoo.modules.module import get_module_resource


class MediaFile(models.Model):
    _inherit = 'clv.mfile'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('clv_mfile', 'static/img', 'mfile_image.png')
        image = base64.b64encode(open(image_path, 'rb').read())
        # return tools.image_process(image, colorize=True)
        return image

    # all image fields are base64 encoded and PIL-supported
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_default_image)

    # resized fields stored (as attachment) for performance
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    image_64 = fields.Image("Image 64", related="image_1920", max_width=64, max_height=64, store=True)
