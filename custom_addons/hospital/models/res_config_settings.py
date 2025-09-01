# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # config params is ir.config_parameter saved
    # you can chaeck on cancel_days http://localhost:8069/odoo/system-parameters?debug=1
    cancel_days = fields.Integer(string='Cancel Days', config_parameter='hospital.cancel_days')
    # delay_alert_contract = fields.Integer(string='Delay alert contract outdated', default=30, config_parameter='hr_fleet.delay_alert_contract')
