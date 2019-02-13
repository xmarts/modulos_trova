# -*- coding: utf-8 -*-
from odoo import http

# class ValidationsModule(http.Controller):
#     @http.route('/validations_module/validations_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/validations_module/validations_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('validations_module.listing', {
#             'root': '/validations_module/validations_module',
#             'objects': http.request.env['validations_module.validations_module'].search([]),
#         })

#     @http.route('/validations_module/validations_module/objects/<model("validations_module.validations_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('validations_module.object', {
#             'object': obj
#         })