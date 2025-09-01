from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # confirm_user_id = fields.Many2one('res.users', string="Confirm User", default=lambda self: self.env.user)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # if self.country_code == 'IN':
        #     invoice_vals['l10n_in_reseller_partner_id'] = self.l10n_in_reseller_partner_id.id
        #     invoice_vals['l10n_in_gst_treatment'] = self.l10n_in_gst_treatment
        print("--------invoice")
        return invoice_vals