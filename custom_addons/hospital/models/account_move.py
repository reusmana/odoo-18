from odoo import models, fields, api, tools, _
# from odoo.tools import date_utils

# abstract model, so we can inherit from other model
# abstract = True artinya model ini tidak akan membuat tabel di database
# class AccountMoveLine(models.AbstractModel):
#     _name = 'contract.models'
#     _description = 'Account Move Line'
#     _abstract = True

#     start_date = fields.Date(string="Start Date",  required=True)
#     # start_date = fields.Date(string="Start Date", default=fields.Date.context_today, required=True)

#     @staticmethod
#     def get_default_start_date():
#         return tools.date_utils.start_of(tools.date_utils.today(), 'month')

#     def get_sale_unit_domain(self):
#         return [('type', '=', 'uom')]


class AccountMove(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    so_confirm_user_id = fields.Many2one('res.users', string="SO Confirm User")

    # def get_sale_unit_domain(self):
    #     return [('type', '=', 'string')]