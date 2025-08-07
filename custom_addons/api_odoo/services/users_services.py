from ..models.users import UsersApi
from odoo import http

class UserServices:
    def __init__(self):
        self.users_api_model = http.request.env['res.users']

    def getUsers(self):
        users = self.users_api_model.sudo().search([])
        return users.read(['id', 'name', 'login']) 