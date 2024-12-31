# -*- coding: utf-8 -*-
from odoo import api, fields, models

class BaseLanguageInstall(models.TransientModel):
    _inherit = "base.language.install"

    def lang_install(self):
        self.ensure_one()
        return super(BaseLanguageInstall, self).lang_install()
