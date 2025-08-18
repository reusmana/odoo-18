# -*- coding: utf-8 -*-
# from odoo import http


# class HospitalInheritance(http.Controller):
#     @http.route('/hospital_inheritance/hospital_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospital_inheritance/hospital_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospital_inheritance.listing', {
#             'root': '/hospital_inheritance/hospital_inheritance',
#             'objects': http.request.env['hospital_inheritance.hospital_inheritance'].search([]),
#         })

#     @http.route('/hospital_inheritance/hospital_inheritance/objects/<model("hospital_inheritance.hospital_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospital_inheritance.object', {
#             'object': obj
#         })

