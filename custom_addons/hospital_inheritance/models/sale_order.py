# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'hospital_inheritance.hospital_inheritance'

    confirm_user_id = fields.Many2one('res.users', string="Confirm User", default=lambda self: self.env.user)

    def action_confirm(self):
        super(SalesOrder, self).action_confirm()
        self.write({'confirm_user_id': 6})

