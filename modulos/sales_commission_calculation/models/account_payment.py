# -*- coding: utf-8 -*-
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, _
from openerp.exceptions import Warning

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    @api.multi
    @api.depends('partner_type')
    def _check_partner_type(self):
        for rec in self:
            if rec.partner_type == 'customer':
                rec.sales_commission_apply = True

    @api.model
    def get_team(self):
        if self._context.get('active_model') and self._context.get('active_model')  == 'account.invoice':
            invoice = self._context.get('active_id', False)
            if invoice:
                inv = self.env['account.invoice'].browse(invoice)
                return inv.team_id.id
        return False

    @api.model
    def get_team_person(self):
        if self._context.get('active_model') and self._context.get('active_model')  == 'account.invoice':
            invoice = self._context.get('active_id', False)
            if invoice:
                inv = self.env['account.invoice'].browse(invoice)
                return inv.user_id.id
        return False
        
    sales_team_id = fields.Many2one(
        'crm.team',
        string='Sales Team',
        reqired=False,
        default=get_team,
    )
    sales_user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=get_team_person,
    )
    commission_manager_id = fields.Many2one(
        'sales.commission.line',
        string='Sales Commission for Manager'
    )
    commission_person_id = fields.Many2one(
        'sales.commission.line',
        string='Sales Commission for Member'
    )
    sales_commission_apply = fields.Boolean(
        string='Sales Commission Apply',
        compute='_check_partner_type',
        store=True,
    )
    
    @api.multi
    def get_teamwise_commission(self):
        sum_line_manager = []
        sum_line_person = []
        amount_person, amount_manager = 0.0, 0.0
        for payment in self:
            if not payment.sales_team_id:
                raise Warning(_('Plaese select Sales Team.'))
            if not payment.sales_user_id:
                raise Warning(_('Plaese select Sales User.'))
            if payment.invoice_ids:
                for invoice in payment.invoice_ids:
                    sum_line_manager.append((payment.amount * invoice.team_id.sales_manager_commission)/100)
                    sum_line_person.append((payment.amount * invoice.team_id.sales_person_commission)/100)
                amount_manager = sum(sum_line_manager)
                amount_person = sum(sum_line_person)
            else:
                amount_manager = (payment.amount * payment.sales_team_id.sales_manager_commission)/100
                amount_person =  (payment.amount * payment.sales_team_id.sales_person_commission)/100
        return amount_person, amount_manager

    @api.multi
    def create_commission(self, amount, commission, type):
        commission_obj = self.env['sales.commission.line']
        product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
        for payment in self:
            if payment.invoice_ids:
                for invoice in payment.invoice_ids:
                #Salesperson
                    if amount != 0.0:
                        commission_value = {
                           # 'sales_team_id': invoice.team_id.id,
                            #'commission_user_id': invoice.user_id.id,
                            'amount': amount,
                            'origin': payment.name,
                            'type':type,
                            'product_id': product.id,
                            'date' : payment.payment_date,
                            'src_payment_id': payment.id,
                            'sales_commission_id':commission.id,
                        }
                        commission_id = commission_obj.create(commission_value)
                        if type == 'sales_person':
                            payment.commission_person_id = commission_id.id
                        if type == 'sales_manager':
                            payment.commission_manager_id = commission_id.id
            else:
                if amount != 0.0:
                    commission_value = {
                        #'sales_team_id': payment.team_id.id,
                        #'commission_user_id': payment.user_id.id,
                        'amount': amount,
                        'origin': payment.name,
                        'type':type,
                        'product_id': product.id,
                        'date' : payment.payment_date,
                        'src_payment_id': payment.id,
                        'sales_commission_id':commission.id,
                    }
                    commission_id = commission_obj.create(commission_value)
                    if type == 'sales_person':
                        payment.commission_person_id = commission_id.id
                    if type == 'sales_manager':
                        payment.commission_manager_id = commission_id.id
        return True
    
    
    
    @api.multi
    def create_base_commission(self, type):
        commission_obj = self.env['sales.commission']
        product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
        for order in self:
            if type == 'sales_person':
                user = order.sales_user_id.id
            if type == 'sales_manager':
                user = order.sales_team_id.user_id.id

            today = date.today()
            first_day = today.replace(day=1)
            last_day = datetime.datetime(today.year,today.month,1)+relativedelta(months=1,days=-1)
            commission_value = {
                    'start_date' : first_day,
                    'end_date': last_day,
                    'product_id':product.id,
                    'commission_user_id': user,
                }
            commission_id = commission_obj.create(commission_value)
        return commission_id
    
    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
#         when_to_pay = self.env['ir.values'].get_default('sale.config.settings', 'when_to_pay')
        when_to_pay = self.env['ir.config_parameter'].sudo().get_param('sales_commission_calculation.when_to_pay') #odoo11
        if  when_to_pay == 'invoice_payment':
            for payment in self:
                if payment.sales_commission_apply:
#                     commission_based_on = self.env['ir.values'].get_default('sale.config.settings', 'commission_based_on')
                    commission_based_on = self.env['ir.config_parameter'].sudo().get_param('sales_commission_calculation.commission_based_on') #odoo11
                    amount_person, amount_manager = 0.0,0.0
                    if commission_based_on == 'sales_team':
                        amount_person, amount_manager = payment.get_teamwise_commission()
                        commission = self.env['sales.commission'].search([
                            ('commission_user_id', '=', payment.sales_user_id.id),
                            ('start_date', '<', payment.payment_date),
                            ('end_date', '>', payment.payment_date),
                            ('state','=','draft')],limit=1)
                        if not commission:
                            commission = payment.create_base_commission(type='sales_person')
                        payment.create_commission(amount_person, commission, type='sales_person')
                        
                        if not payment.sales_user_id.id == payment.sales_team_id.user_id.id and payment.sales_team_id.user_id:
                            commission = self.env['sales.commission'].search([
                                ('commission_user_id', '=', payment.sales_team_id.user_id.id),
                                ('start_date', '<', payment.payment_date),
                                ('end_date', '>', payment.payment_date),
                                ('state','=','draft')],limit=1)
                            if not commission:
                                commission = payment.create_base_commission(type='sales_manager')
                            payment.create_commission(amount_manager,commission, type='sales_manager')
        return res
        
    @api.multi
    def cancel(self):
        res = super(AccountPayment, self).cancel()
        for rec in self:
            if rec.commission_manager_id:
                rec.commission_manager_id.state = 'exception'
            if rec.commission_person_id:
                rec.commission_person_id.state = 'exception'
        return res
