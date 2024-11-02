from datetime import date
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from dateutil import relativedelta



class HospitalPatient(models.Model):
    _name = "hospital"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order='id desc'


    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="reference", tracking=True,default='example of a default')
    birth_date = fields.Date(string="Birth of Date")
    age = fields.Integer(string=" Age ", tracking=True,compute='_compute_age',
                         inverse='_inverse_compute_age',search='_search_age',readonly=False)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ], string='Gender', tracking=True,default='male')
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one('appointment', string="Appointments")
    image = fields.Image(string="Patient Image")
    tag_ids = fields.Many2many('patient.tag',string="Patient Tag")
    appointment_count = fields.Integer(string="Appointment Count",compute='_compute_appointment_count',store=True)
    appointment_ids = fields.One2many('appointment','patient_id',string="Appointments for count")
    parent = fields.Char(string="Parent")
    marital_states = fields.Selection([('married','Married'),('single','Single')]
                                      ,string="Martial States",tracking=True)
    partner = fields.Char(string="Partner")
    is_birthday = fields.Boolean(string="is birth day",compute='_compute_is_birthday')
    phone=fields.Char(string="Phone number")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    company_id = fields.Many2one('res.company',string="company name")



    @api.depends('appointment_ids') #ORM METHOD
    def _compute_appointment_count(self):
        appointment_group=self.env['appointment'].read_group(domain=[('patient_id','=',self.id)],
                                                             fields=['patient_id'],groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id=appointment.get('patient_id')[0]
            patient_rec=self.browse(patient_id)
            patient_rec.appointment_count = appointment['patient_id_count']
            self -= patient_rec
        self.appointment_count= 0





    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         rec.appointment_count= self.env['appointment'].search_count([('patient_id','=',rec.id)])

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("you can not delete that because there is appointment"))



    @api.model
    def create(self,vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital')
        return super(HospitalPatient,self).create(vals)


    def write(self,vals):
        if not self.ref and not vals.get('ref'):
            vals['ref']=self.env['ir.sequence'].next_by_code('hospital')
        return super(HospitalPatient,self).write(vals)


    @api.constrains('birth_date')
    def check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date > fields.Date.today():
                raise ValidationError(_("THE DATE YOU HAD ENTERED IS NOT ACCEPTABLE!"))


    @api.depends('birth_date')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.birth_date:
                today=date.today()
                if today.day == rec.birth_date.day and today.month == rec.birth_date.month:
                    is_birthday = True
            rec.is_birthday = is_birthday



    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 1

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.birth_date = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self,operator,value):
        birth_date = date.today() - relativedelta.relativedelta(years=value)
        start_of_year=birth_date.replace(day=1,month=1)
        end_of_year=birth_date.replace(day=31,month=12)
        return [('birth_date','>=',start_of_year),('birth_date','<=',end_of_year)]



    def name_get(self):
        return [(record.id, "[%s] %s" %(record.ref , record.name)) for record in self]

    #or

    # def name_get(self):
    #     patient_list=[]
    #     for record in self:
    #         name= record.ref + ' ' + record.name
    #         patient_list.append((record.id,name))
    #     return patient_list



    #-------buttons--------#
    def action_view_appointment(self):
        return {
            'name': _('Appointments'),
            'res_model': 'appointment',
            'view_mode': 'list,form,activity,calendar',
            'domain': [('patient_id','=',self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id':self.id},
        }
    def just_test_group(self):
        return {
            'effect': {
                'fadeout': 'slow', # fadeout bt5leha disappear b3d kam second automatic
                'message': 'click done successfully',
                'type': 'rainbow_man',
            }
        }