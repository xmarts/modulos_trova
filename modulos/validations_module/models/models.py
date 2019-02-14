# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import UserError, ValidationError

class ValidVenta(models.Model):
	_inherit = 'sale.order'

	state = fields.Selection([
		('draft','Presupuesto'),
		('sent','Presupuesto Enviado'),
		('to_validate','Validado'),
		('sale','Pedido de Ventas'),
		('done','Bloqueado'),
		('cancel','Cancelado')
		])

	@api.one
	def action_validate(self):
		self.write({'state': 'to_validate'})

	"""
	@api.depends('cocina','clg','piso','proteccion','avalcat','aca')
	def _total_mejoras(self):
	    self.precio_mejoras = (float(self.cocina)) + (float(self.clg)) + (float(self.piso)) + (float(self.proteccion)) + (float(self.avalcat)) + (float(self.aca))
	"""

class ValidFacture(models.Model):
	_inherit = 'sales.commission'

	state = fields.Selection([
		('draft','Presupuesto'),
		('to_validate','Validado'),
		('invoice','Facturado'),
		('cancel','Cancelado')
		])

	@api.one
	def action_validate2(self):
		self.write({'state':'to_validate'})

class ValidTitulacion(models.Model):
	_inherit = 'trova.vivienda.titu'

	etapas = fields.Selection([
		('Disponible', 'Disponible'),
		('Invadida', 'Invadida'),
		('Poravaluo', 'Por avalúo'),
		('Porfirma', 'Por firmar'),
		('Firmada', 'Firmada'),
		('Cancelada', 'Cancelada')
		], default='Disponible')

	@api.one
	def action_validate(self):
		self.write({'etapas':'Disponible'})

	@api.one
	def action_validate1(self):
		self.write({'etapas':'Invadida'})

	@api.one
	def action_validate2(self):
		self.write({'etapas':'Poravaluo'})

	@api.one
	def action_validate3(self):
		self.write({'etapas':'Porfirma'})

	@api.one
	def action_validate4(self):
		self.write({'etapas':'Firmada'})

	@api.one
	def action_validateCancell(self):
		self.write({'etapas':'Cancelada'})

	"""@api.depends('num_cuenta')
	@api.onchange('cuenta_select')
	def pruebaVal(self):
		if self.folio.prop_vivienda.cuenta_select:
			valor = self.folio.prop_vivienda.cuenta_select.acc_number
			self.num_cuenta = valor
			if valor == self.folio.prop_vivienda.cuenta_select.acc_number:
				raise UserError('coinciden')
			else: 
				raise UserError('No coinciden')
		else:
			raise UserError('El propietario no tiene ninguna cuenta seleccionada')"""
		


class ValidPrecio(models.Model):
	_inherit = 'trova.vivienda'

	etapas = fields.Selection([
		('Disponible', 'Disponible'),
		('Invadida', 'Invadida'),
		('Borrador', 'Borrador'),
		('Poravaluo', 'Por avalúo'),
		('Porfirma', 'Por firmar'),
		('Firmada', 'Firmada'),
		('Cancelada', 'Cancelada')
		], default='Disponible')

	@api.one
	def action_validate(self):
		self.write({'etapas':'Disponible'})

	@api.one
	def action_validate1(self):
		self.write({'etapas':'Invadida'})

	@api.one
	def action_validateBor(self):
		self.write({'etapas':'Borrador'})
	
	@api.one
	def action_validate2(self):
		self.write({'etapas':'Poravaluo'})

	@api.one
	def action_validate3(self):
		self.write({'etapas':'Porfirma'})

	@api.one
	def action_validate4(self):
		self.write({'etapas':'Firmada'})

	@api.one
	def action_validateCancell(self):
		self.write({'etapas':'Cancelada'})
					
class ValidPago(models.Model):
	_inherit = 'trova_employee.trova_model'

	state = fields.Selection([
		('draft','Borrador'),
		('open','Abierto'),
		('aprove', 'Aprovado'),
		('paid','Pagado'),
		('cancel','Cancelado')
		])
	
	@api.one
	def action_aprove(self):
		self.write({'state':'aprove'})

class AddCampCuent(models.Model):
	_inherit = 'res.partner'

	cuenta_select = fields.Many2one('res.partner.bank', string="Selecciona tu cuenta", required=False)
		
