from odoo import api, fields, models, time, exceptions, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model"
	_description = "Pagos por destajo"

	@api.depends('option_lines1')
	def _tot1_concepto(self):
		self.total_g1 = sum(line.sub_total for line in self.option_lines1)

	@api.depends('option_lines2')
	def _tot2_concepto(self):
		self.total_g2 = sum(line.sub_total for line in self.option_lines2)

	@api.depends('option_lines3')
	def _tot3_concepto(self):
		self.total_g3 = sum(line.sub_total for line in self.option_lines3)

	@api.depends('option_lines4')
	def _tot4_concepto(self):
		self.total_g4 = sum(line.sub_total for line in self.option_lines4)

	
	def _name_default(self):
		cr = self.env.cr
		cr.execute('select "id" from "trova_employee_trova_model" order by "id" desc limit 1')
		id_returned = cr.fetchone()
		if id_returned == None:
			id_returned = (0,)
		return "Pago {}".format(max(id_returned)+1)

	@api.multi
	def action_payment_open(self):
		if not self.option_lines1 and not self.option_lines2 and not self.option_lines3 and not self.option_lines4:
			raise UserError(_('Por favor, cree algunas líneas de conceptos.'))
		return self.write({'state': 'open'})

	@api.multi
	def action_payment_paid(self):
		return self.write({'state': 'paid'})

	@api.multi
	def action_payment_cancel(self):
		return self.write({'state': 'cancel'})

	@api.multi
	def action_payment_draft(self):
		return self.write({'state': 'draft'})

	name = fields.Char(string='Titulo del pago', default=_name_default)
	employee_id = fields.Many2one('hr.employee', string='Habilitador', required=True, readonly=True, states={'draft': [('readonly', False)]})
	vivienda_id = fields.Many2one('trova.vivienda',string='Vivienda', required=True)
	date_start = fields.Date(string='Semana del', default=fields.Datetime.now, index=True, copy=False, readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	date_finish = fields.Date(string='Al', index=True, copy=False, readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	state = fields.Selection([
		('draft','Borrador'),
		('open', 'Abierto'),
		('paid', 'Pagado'),
		('cancel', 'Cancelado'),
		], string='Estatus', index=True, readonly=True, default='draft', track_visibility='onchange', copy=False)
	option_lines1 = fields.One2many('trova_employee.trova_model2', 'option_id', string='Option lines', readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	option_lines2 = fields.One2many('trova_employee.trova_model3', 'option_id', string='Option lines', readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	option_lines3 = fields.One2many('trova_employee.trova_model4', 'option_id', string='Option lines', readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	option_lines4 = fields.One2many('trova_employee.trova_model5', 'option_id', string='Option lines', readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]})
	#currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
	total_g1 = fields.Float(string='Total', compute="_tot1_concepto")
	total_g2 = fields.Float(string='Total', compute="_tot2_concepto")
	total_g3 = fields.Float(string='Total', compute="_tot3_concepto")
	total_g4 = fields.Float(string='Total', compute="_tot4_concepto")


class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model2"
	_description = "Pagos por destajo2"

	@api.one
	@api.depends('price_unit', 'qty', 'option')
	def _subtotgeneral_concepto(self):
		self.sub_total = self.qty * self.price_unit

	@api.onchange('option')
	def _onchange_product_id(self):
		if self.option:
			self.price_unit = self.option.price_unit


	option_id = fields.Many2one('trova_employee.trova_model', string='Campo Many2one', required=True, ondelete='cascade',
		index=True, copy=False)
	option = fields.Many2one('trova_employee.trova_model6', string='Concepto', ondelete='restrict')
	qty= fields.Integer(string='Cantidad', readonly=False)
	price_unit = fields.Float(string='Precio', readonly=False)
	sub_total = fields.Float(string='Total', readonly=True, compute="_subtotgeneral_concepto")


class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model3"
	_description = "Pagos por destajo3"

	@api.one
	@api.depends('price_unit', 'qty', 'option')
	def _subtotgeneral_concepto(self):
		self.sub_total = self.qty * self.price_unit

	@api.onchange('option')
	def _onchange_product_id(self):
		if self.option:
			self.price_unit = self.option.price_unit

	option_id = fields.Many2one('trova_employee.trova_model', string='Campo Many2one', required=True, ondelete='cascade',
		index=True, copy=False)
	option = fields.Many2one('trova_employee.trova_model6', string='Concepto', ondelete='restrict')
	qty= fields.Integer(string='Cantidad', readonly=False)
	price_unit = fields.Float(string='Precio', readonly=False)
	sub_total = fields.Float(string='Total', readonly=True, compute="_subtotgeneral_concepto")

class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model4"
	_description = "Pagos por destajo4"

	@api.one
	@api.depends('price_unit', 'qty', 'option')
	def _subtotgeneral_concepto(self):
		self.sub_total = self.qty * self.price_unit

	@api.onchange('option')
	def _onchange_product_id(self):
		if self.option:
			self.price_unit = self.option.price_unit

	option_id = fields.Many2one('trova_employee.trova_model', string='Campo Many2one', required=True, ondelete='cascade',
		index=True, copy=False)
	option = fields.Many2one('trova_employee.trova_model6', string='Concepto', ondelete='restrict')
	qty= fields.Integer(string='Cantidad', readonly=False)
	price_unit = fields.Float(string='Precio', readonly=False)
	sub_total = fields.Float(string='Total', readonly=True, compute="_subtotgeneral_concepto")

class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model5"
	_description = "Pagos por destajo5"

	@api.one
	@api.depends('price_unit', 'qty', 'option')
	def _subtotgeneral_concepto(self):
		self.sub_total = self.qty * self.price_unit

	@api.onchange('option')
	def _onchange_product_id(self):
		if self.option:
			self.price_unit = self.option.price_unit

	option_id = fields.Many2one('trova_employee.trova_model', string='Campo Many2one', required=True, ondelete='cascade',
		index=True, copy=False)
	option = fields.Many2one('trova_employee.trova_model6', string='Concepto', ondelete='restrict')
	qty= fields.Integer(string='Cantidad', readonly=False)
	price_unit = fields.Float(string='Precio', readonly=False)
	sub_total = fields.Float(string='Total', readonly=True, compute="_subtotgeneral_concepto")

class TrovaEmployee(models.Model):
	_name = "trova_employee.trova_model6"
	_description = "Pagos por destajo6"

	name = fields.Char(string='Concepto', required=True, index=True)
	price_unit = fields.Float(string='Precio', required=True, readonly=False)