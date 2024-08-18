from odoo import api, fields, models, _



class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    _rec_name='operation_name'
    _order='sequence,id'

    doctor_id=fields.Many2one('res.users', string="Doctor",required=False)
    operation_name=fields.Char(string="Name")
    reference_record=fields.Reference(selection=[('hospital','Patient'),('appointment','Appointment')],string="Record")
    sequence=fields.Integer(string="Sequence",default=10)

    def name_create(self,name):
        return self.create({'operation_name': name}).name_get()[0]
