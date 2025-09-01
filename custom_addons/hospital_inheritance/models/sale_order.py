# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'hospital_inheritance.hospital_inheritance'

    confirm_user_id = fields.Many2one('res.users', string="Confirm User", default=lambda self: self.env.user)

    def action_confirm(self):
        super(SalesOrder, self).action_confirm()
        self.write({'confirm_user_id': 6})

    def _prepare_invoice(self):
        invoice_vals = super(SalesOrder, self)._prepare_invoice()
        # if self.country_code == 'IN':
        #     invoice_vals['l10n_in_reseller_partner_id'] = self.l10n_in_reseller_partner_id.id
        #     invoice_vals['l10n_in_gst_treatment'] = self.l10n_in_gst_treatment
        print("--------invoice")
        if self.confirm_user_id:
            invoice_vals['so_confirm_user_id'] = self.confirm_user_id.id
        return invoice_vals

