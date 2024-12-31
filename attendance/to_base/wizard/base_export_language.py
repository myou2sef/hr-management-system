# -*- coding: utf-8 -*-
import base64
import os
import tempfile
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class BaseLanguageExport(models.TransientModel):
    _name = "base.language.export"
    _description = "Language Export"

    name = fields.Char('File Name', readonly=True)
    lang = fields.Selection(lambda self: self._get_languages(), string='Language', required=True)
    format = fields.Selection([('csv', 'CSV File'), ('po', 'PO File')], string='File Format', required=True, default='po')
    modules = fields.Many2many('ir.module.module', 'rel_modules_langexport', 'wiz_id', 'module_id',
                             string='Apps To Export', domain=[('state', '=', 'installed')])
    data = fields.Binary('File', readonly=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    def _get_languages(self):
        langs = self.env['res.lang'].get_installed()
        return langs

    def act_getfile(self):
        self.ensure_one()
        lang = self.lang
        mods = sorted(self.mapped('modules.name')) or ['all']

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, 'temp.po' if self.format == 'po' else 'temp.csv')
            tools.trans_export(lang, mods, temp_file, self.format, self._cr)
            
            with open(temp_file, 'rb') as buf:
                out = base64.b64encode(buf.read())

        filename = mods[0] if len(mods) == 1 else 'new'
        extension = self.format
        name = f"{filename}.{extension}"
        
        self.write({
            'state': 'get',
            'data': out,
            'name': name
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'base.language.export',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
