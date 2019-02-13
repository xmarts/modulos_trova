# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class CrmLeadRestriction(models.Model):
  _inherit = 'crm.lead'


  @api.model
  def create(self,vals):
    fc = datetime.today() + timedelta(days=-15)
    b = str(fc)
    cr = self.env.cr
    sql ="select * from crm_lead  where partner_id='"+str(vals.get('partner_id'))+"' and active='t' and create_date >'"+b+"' limit 1"
    cr.execute(sql)
    id_returned = cr.fetchone()
    
    if id_returned:
    	raise exceptions.ValidationError('Existe una oportunidad abierta para este cliente, si es un error consulte al administrador.')

     

    return super(CrmLeadRestriction, self).create(vals)
