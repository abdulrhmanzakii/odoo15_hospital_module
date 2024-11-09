import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'


    name = fields.Char(string="Reference")
    patient_id = fields.Many2one('hospital', string="patient",ondelete='restrict')
    active = fields.Boolean(string="Active", default=True)
    appointment_time = fields.Datetime(string="Appointment Time",default=fields.Datetime.now)
    booking_date= fields.Date(string="Booking Date", default=fields.Date.context_today)
    gender = fields.Selection(related='patient_id.gender',readonly=False)
    ref = fields.Char(string="reference of patient", tracking=True)
    prescription = fields.Html(string="prescription")
    doctor_id = fields.Many2one('res.users',string='Doctor',tracking=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('canceled', 'Canceled')], string="Statues",required=True,default='draft',tracking=True)

    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines','appointment_id',string="Pharmacy Lines")
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    image = fields.Image(related='patient_id.image')
    operation_id=fields.Many2one('hospital.operation',string="Operations")
    progress=fields.Integer(string="Progress",compute='_compute_progress')
    duration=fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company) # price unit,price list

    currency_id = fields.Many2one('res.currency', string='Currency',related='company_id.currency_id') # currency EUR OR USD
    amount_total=fields.Monetary(string='Total Price',currency_feild='currency_id',compute='_compute_amount_total')
    note=fields.Html(string="Note")
    test_field= fields.Binary(string="Binary Field")




    @api.depends('pharmacy_line_ids')
    def _compute_amount_total(self):
        for rec in self:
            amount_total=0
            for line in rec.pharmacy_line_ids:
                amount_total += line.price_sub_total
            rec.amount_total = amount_total






    @api.onchange('patient_id')
    def _patient_id_(self):
        self.ref = self.patient_id.ref

    def object_button(self):
        return {
            'type': 'ir.actions.act_url',
            'target':'new',
            'url': 'https://web5.topcinema.top',


        }
    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('click to open patient record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital',
                }],
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital',
                    'res_id': self.patient_id.id,
                    'views': [(False,'form')]

                }
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def send_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_('the patient does not have phone number'))
        message ='Hello *%s* , your *Appointment* is: %s , Thank you!' % (self.patient_id.name,self.name)
        whatsapp_link='https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone,message)
        self.message_post(body=message,subject='Whats app message')

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_link,
        }
    def send_mail(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if  rec.patient_id.email:
                template.send_mail(rec.id, force_send = True)
            else:
                raise ValidationError(_("patient Does not Have Email "))

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow', # fadeout bt5leha disappear b3d kam second automatic
                'message': 'Done',
                'type': 'rainbow_man',
            }
        }

    def action_canceled(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'



    def write(self,vals):
        if not self.name and not vals.get('name'):
            vals['name'] =self.env['ir.sequence'].next_by_code('appointment')
        return super(HospitalAppointment,self).write(vals)




    @api.model
    def create(self,vals):
        vals['name']= self.env['ir.sequence'].next_by_code('appointment')
        self = super(HospitalAppointment,self).create(vals)
        sl_no=0
        for line in self.pharmacy_line_ids:
            sl_no +=1
            line.sl_no = sl_no
        return self


    def write(self, values):
        res = super(HospitalAppointment, self).write(values)
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res


    def unlink(self):
        for rec in self:
            if rec.state != 'canceled':
                raise ValidationError(_("you can not delete this !"))
        return super(HospitalAppointment,self).unlink()


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress= random.randrange(0,25)
            elif rec.state == 'in_consultation':
                progress= random.randrange(25,99)
            elif rec.state == 'done':
                progress=100
            else:
                progress=0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "appointment pharmacy lines"

    sl_no = fields.Integer(string="PNo.")
    product_id = fields.Many2one('product.product',required=True)
    price_unit =fields.Float(related='product_id.list_price',default=0.0)
    qty = fields.Float(string="Quantity",default=1)
    appointment_id =fields.Many2one('appointment',string="Appointment")
    company_currency_id = fields.Many2one('res.currency', string='Currency',related='appointment_id.currency_id')
    price_sub_total = fields.Monetary(string="Subtotal",compute='_compute_price_sub_total'
                                      ,currency_field='company_currency_id')

    @api.model_create_multi
    def create(self, vals):
        appointments = super(AppointmentPharmacyLines, self).create(vals)
        for appointment in appointments:
            msg = f"A New Product Recently {appointment.product_id.name} Has Been Add"
            appointment.appointment_id.message_post(body=msg)

        return appointments

    def write(self, vals):
        self._log_access_tracking(vals)

        return super().write(vals)

    def _log_access_tracking(self, vals):
        template_id = 'om_hospital.track_appointment_template'
        for rec in self:
            data = {}
            if 'product_id' in vals:
                data.update({'product_id': self.env["product.product"].browse(vals.get('product_id')).name})

            if 'qty' in vals:
                data.update({'qty': vals.get('qty')})

            if 'price_unit' in vals:
                data.update({'price_unit': vals.get('price_unit')})

            if data:
                rec.appointment_id.message_post_with_view(template_id, values={'rec': rec, 'data': data})




    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit =self.product_id.lst_price

    @api.depends('price_unit','qty')
    def _compute_price_sub_total(self):
        for rec in self:
            rec.price_sub_total = rec.price_unit * rec.qty

