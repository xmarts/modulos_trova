# -*- coding: utf-8 -*-
from odoo import http

# class ViviendaNew(http.Controller):
#     @http.route('/vivienda_new/vivienda_new/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vivienda_new/vivienda_new/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vivienda_new.listing', {
#             'root': '/vivienda_new/vivienda_new',
#             'objects': http.request.env['vivienda_new.vivienda_new'].search([]),
#         })

#     @http.route('/vivienda_new/vivienda_new/objects/<model("vivienda_new.vivienda_new"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vivienda_new.object', {
#             'object': obj
#         })