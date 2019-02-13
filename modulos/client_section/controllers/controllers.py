# -*- coding: utf-8 -*-
from odoo import http

# class ClientSection(http.Controller):
#     @http.route('/client_section/client_section/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_section/client_section/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_section.listing', {
#             'root': '/client_section/client_section',
#             'objects': http.request.env['client_section.client_section'].search([]),
#         })

#     @http.route('/client_section/client_section/objects/<model("client_section.client_section"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_section.object', {
#             'object': obj
#         })