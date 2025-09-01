# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = 'sale.report'

    confirm_user_id = fields.Many2one('res.users', string="Confirm User", default=lambda self: self.env.user)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['confirm_user_id'] = "so.confirm_user_id"
        return res

