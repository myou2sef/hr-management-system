# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def get_currency_rates(self, company, currency_ids, date):
        Currency = self.env['res.currency']
        res = {currency.id: currency.rate for currency in Currency.browse(currency_ids)}
        return res

    font = fields.Selection(selection_add=[('Times New Roman', 'Times New Roman')])
