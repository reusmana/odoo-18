from ..services.users_services import UserServices
from odoo import http
from odoo.http import request
from json import loads

class UserController(http.Controller):

    @http.route('/api/odoo/test', type="json", auth="public")
    def test(self, **kwargs):
        return {"message": "Hello from Odoo JSON"}

    @http.route('/api/odoo/auth', type="json", auth="public", cors="*")
    def login(self, **kwargs):
        if(request.httprequest.method == 'POST'):
            print(f"ags {kwargs['username']}" ) #ags {'db': 'odoo18', 'username': 'reusmanasujani@gmail.com', 'password': 'reussujani'}
            data = loads(request.httprequest.data).get('params')
            print(data.get('username'))
            username = data.get('username')
            password = data.get('password')
            credential = {'login': username, 'password': password, 'type': 'password'}
            request.session.authenticate(request.db, credential)

            request.future_response.set_cookie(
                    'session_id', request.session.sid,
                    max_age=http.get_session_max_inactivity(env), httponly=True
                )
            response = {
                "code": 200,
                "message": "Success",
                "session": request.session.sid
            }
            return response
        else:
            return {"message": "Hello from Odoo JSON"}
    
    @http.route('/api/odoo/users', type="json", auth="user", cors="*")
    def getUsers(self, params=None, **kwargs):
        print(http.request.httprequest.data)
        data = loads(http.request.httprequest.data).get('data')
        print(data.get('username'))
        print(kwargs)
        response = {
            "code": 200,
            "message": "Success",
            "data": UserServices().getUsers()
        }
        return response