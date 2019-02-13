# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

class comision_vendedor(models.Model):
	_inherit = 'trova.vivienda.titu'

	comision_vendedor=fields.Float(string='Comision del Vendedor')
	invoice_id=fields.Many2one('account.invoice',string='Factura', readonly=True)
	invoice_state= fields.Selection(selection=[('draft', 'Borrador'),('open', 'Abierto'),('paid', 'Pagado'),('cancel', 'Cancelado') ],string='Estado', related="invoice_id.state",default='draft', readonly=True)
	

	@api.multi
	def get_teamwise_commission(self):
		sum_line_manager = []
		sum_line_person = []
		amount_person, amount_manager = 0.0, 0.0
		for vivienda in self:
			# if not vivienda.member_ids:
			# 	raise Warning(_('Plaese select Sales Team.'))
			# if not vivienda.asesor:
			# 	raise Warning(_('Plaese select Sales User.'))

			amount_person = (vivienda.precio_vivienda * (vivienda.comision_vendedor/100))

		return amount_person, amount_manager

	

	@api.multi
	def create_base_commission(self, type):
		commission_obj = self.env['sales.commission']
		product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
		for order in self:
			if type == 'sales_person':
				user = order.asesor.id

			today = date.today()
			first_day = today.replace(day=1)
			last_day = datetime(today.year,today.month,1)+relativedelta(months=1,days=-1)
			commission_value = {
					'start_date' : first_day,
					'end_date': last_day,
					'product_id':product.id,
					'commission_user_id': user,
				}
			commission_id = commission_obj.create(commission_value)
		return commission_id

	@api.multi
	def create_commission(self, amount, commission, type, factura):
		commission_obj = self.env['sales.commission.line']
		product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
		for vivienda in self:
			if amount != 0.0:
				commission_value = {
				# 'sales_team_id': invoice.team_id.id,
					'commission_user_id': vivienda.asesor.id,
					'amount': amount,
					'amount_company_currency': amount,
					'origin': vivienda.name,
					'type':type,
					'product_id': product.id,
					'date' : datetime.now(),
					'src_invoice_id': factura,
					'sales_commission_id':commission.id,
				}
				commission_id = commission_obj.create(commission_value)
				if type == 'sales_person':
					vivienda.commission_person_id = commission_id.id
		return True

	@api.multi
	def action_titu_invoice_create(self):
		invoice_obj = self.env["account.invoice"]
		invoice_line_obj = self.env["account.invoice.line"]

		for vivienda in self:
			# Create Invoice
			if vivienda.invoice_state == 'cancel' or not vivienda.invoice_state:
				if vivienda.folio and vivienda.presupuesto:
					curr_invoice = {
						'partner_id': vivienda.cliente.id,
						'account_id': vivienda.cliente.property_account_receivable_id.id,
						'state': 'draft',
						'type': 'out_invoice',
						'date_invoice': datetime.now(),
						'origin': vivienda.name,
						'target': 'new',
						'name': 'FACTTIT' + str(vivienda.id),
					}

					inv_ids = invoice_obj.create(curr_invoice)
					inv_id = inv_ids.id
					vivienda.invoice_id = inv_id

					if inv_ids:
						prd_account_id = self._default_account()
						# Create Invoice line
						curr_invoice_line = {
							'name': "Cargo por Vivienda con Folio Real: " + str(vivienda.folio.name),
							'price_unit': vivienda.total_pagar or 0,
							'quantity': 1.0,
							'account_id': prd_account_id,
							'invoice_id': inv_id,
						}

						inv_line_ids = invoice_line_obj.create(curr_invoice_line)

					amount_person, amount_manager = 0.0,0.0
					amount_person, amount_manager = vivienda.get_teamwise_commission()
					commission = self.env['sales.commission'].search([
							('commission_user_id', '=', vivienda.asesor.id),
							('start_date', '<', str(datetime.now())),
							('end_date', '>', str(datetime.now())),
							('state','=','draft')],limit=1)
					if not commission:
						commission = vivienda.create_base_commission(type='sales_person')
						vivienda.create_commission(amount_person, commission, type='sales_person', factura=inv_id)
					if commission:
						vivienda.create_commission(amount_person, commission, type='sales_person', factura=inv_id)
					    
						

					return {
						'domain': "[('id','=', " + str(inv_id) + ")]",
						'name': 'vivienda Invoice',
						'view_type': 'form',
						'view_mode': 'tree,form',
						'res_model': 'account.invoice',
						'type': 'ir.actions.act_window'
					}
	