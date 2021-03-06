# -*- coding: utf-8 -*-

from odoo import models, fields, api

class vivienda__add(models.Model):
	
	_inherit = 'trova.vivienda'
	precio_de_venta = fields.Boolean(string='Precio de Venta',  help='Precio de Venta')
	precio_venta = fields.Float(string='Precio de la venta')
	terreno_excedente = fields.Boolean(string='Terreno Excedente',  help='Terreno Excedente')
	precio_terreno_excedente = fields.Float(string='Precio del Terreno Excedente')
	ISR = fields.Integer(string='ISR')
	account_analytic_id=fields.Many2one('account.analytic.account',string='Cuenta Analitica')


class contac_add(models.Model):
	_inherit ='res.partner'
	_sql_constraints = [(
		'curp_unique',
		'unique(curp)',
		'la CURP ya existe, favor de modificarla'
		),
		(
		'nss_unique',
		'unique(nss)',
		'el NSS ya existe, favor de modificarlo'
		)]

class conyuge_adjuntos(models.Model):
	_inherit= 'sale.order'

	curp_doc_c = fields.Binary(string='Curp')
	ine_doc_c = fields.Binary(string='INE')
	acta_doc_c = fields.Binary(string='Acta de Nacimiento')
	acta_esposa_doc_c = fields.Binary(string='Acta de Nacimiento Esposa(o)', help="En caso de estar casado adjuntar acta de la esposa(o)")
	acta_matrimonio_doc_c = fields.Binary(string='Acta de Matrimonio')
	rfc_doc_c = fields.Binary(string='RFC')
	bansefi_doc_c = fields.Binary(string='BANSEFI')
	precalificacion_doc_c = fields.Binary(string='Pre Calificacion')
	constancia_taller_doc_c = fields.Binary(string='Constancia de Taller')
	comp_domicilio_doc_c = fields.Binary(string='Comprobante de Domicilio')
	credito_con = fields.Boolean(related='partner_id.credito_conyu', string="conyu" ,readonly=True)

class purchase_vivienda(models.Model):
	_inherit='purchase.order.line'


	@api.model
	def create(self, vals):
		res=super(purchase_vivienda, self).create(vals)	
	

		r = vals.get("amount_total_fac")
		if res:
			total=res.price_subtotal + res.price_tax
			ini=res.account_analytic_id.name
			ini_id=res.account_analytic_id.id
			do=self.env['trova.vivienda'].create({'name':ini,'preciocompra':total,'recamaras':0,'account_analytic_id':ini_id})
				
		return res