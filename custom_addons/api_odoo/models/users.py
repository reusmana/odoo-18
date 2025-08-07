from odoo import models, fields, api, _

class UsersApi(models.Model):
    _name = 'users.api'
    _description = 'User Api'

    api_key = fields.Char(string="API Key")
    api_secret = fields.Char(string="API Secret")
    api_token = fields.Char(string="API Token")
    api_token_secret = fields.Char(string="API Token Secret")
    user_id = fields.Many2one('res.users', string="User")


class UserInheritance(models.Model):
    _inherit = 'res.users'

    userapi_ids = fields.One2many('users.api', 'user_id', string="User APIs")
