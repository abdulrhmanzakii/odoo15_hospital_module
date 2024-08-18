from odoo import api, fields, models,_


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Nmae",required=True,trim=False)
    active = fields.Boolean(string="Active" , default=True ,copy=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence=fields.Integer(string="Sequence")
    tag_information=fields.Char(string="Tag Information",default="the tag information here",copy=False)

    def copy(self, default=None):
        if default is None:
            default={}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        default['sequence']=10
        return super(PatientTag,self).copy(default)



    _sql_constraints = [
        ('name_tag_uniq', 'unique (name)', "Tag name already exists !"),
        ('check_seq', 'check (sequence > 0)', "sequence must be non zero and positive number")
    ]