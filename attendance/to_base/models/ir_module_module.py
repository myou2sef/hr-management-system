# -*- coding: utf-8 -*-
import glob
import os.path
from odoo import models, api, tools
from odoo.modules import get_module_path


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def _update_translations(self, filter_lang=None, overwrite=False):
        res = super()._update_translations(filter_lang=filter_lang, overwrite=overwrite)
        
        if 'to_base' in self.mapped('name'):
            langs = filter_lang or self.env['res.lang'].get_installed()
            self._update_module_infos_translation(langs, overwrite=overwrite)
        
        return res

    def _update_module_infos_translation(self, langs, overwrite=False):
        """Update module translations from i18n_extra directory."""
        if not isinstance(langs, (list, set)):
            langs = [langs]

        modules_name = set(self.mapped('name'))
        i18n_extra_path = os.path.join(get_module_path('to_base'), 'i18n_extra')
        
        if not os.path.exists(i18n_extra_path):
            return

        for lang in langs:
            i18n_extra_files = glob.glob(os.path.join(i18n_extra_path, f'*.po'))
            for file_path in i18n_extra_files:
                module_name = os.path.basename(file_path).split(f'_{lang}')[0]
                if module_name in modules_name:
                    tools.trans_load(
                        self.env.cr,
                        file_path,
                        lang,
                        verbose=False,
                        create_empty_translation=False,
                        overwrite=overwrite
                    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if records:
            langs = self.env['res.lang'].get_installed()
            records._update_module_infos_translation(langs)
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in ['shortdesc', 'summary', 'description']):
            langs = self.env['res.lang'].get_installed()
            self._update_module_infos_translation(langs, overwrite=True)
        return res
