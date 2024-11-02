import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class RoportAppointment(models.TransientModel):
    _name = "report.appointment.wizard"
    _description = "report Appointment Wizard"



    patient_id = fields.Many2one('hospital', string="Patient")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    appointment_id = fields.Many2one('appointment',string="appointment")


    def print_button(self):
        domain=[]
        patient_id=self.patient_id
        if patient_id:
            domain += [('patient_id' , '=' , patient_id.id)]
        date_from = self.date_from
        if date_from :
            domain += [('appointment_time','>=',date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('appointment_time','<=',date_to)]

        appointments = self.env['appointment'].search_read(domain)
        data = {
            'form': self.read()[0],
            'appointments': appointments,

        }

        return self.env.ref('om_hospital.report_appointment').report_action(self, data=data)


# def action_print_report(self):
    # data = {
    #     # 'form': self.read()[0],
    #
    # }
    # return self.env.ref('om_hospital.report_appointment').report_action(self, data=data)
