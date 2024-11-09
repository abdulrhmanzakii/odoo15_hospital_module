from odoo import api, fields, models


class ReportPatientCard(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_id_card'
    _description = 'Patient Card Report.'

    @api.model
    def _get_report_values(self, docids, data=None):
        appointments = self.env['appointment'].search([('patient_id','=',docids[0])])
        print("docides",docids)
        appointment_list=[]
        for app in appointments:
            vals = {
                "name" : app.name,
                "doctor_id": app.doctor_id.name,
                "appointment_time": app.appointment_time,
            }

            appointment_list.append(vals)



        return {
            'doc_ids' : docids,
            'doc_model' : self.env['hospital'],
            'data' : data,
            'docs' : self.env['hospital'].browse(docids[0]),
            'appointment':appointment_list,
        }
    #
    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     docs = self.env['employee.penalty'].browse(docids)
    #     docs_done = docs.filtered(lambda d: d.state == 'done')
    #
    #     if not docs_done:
    #         raise UserError('You cannot print this report unless the status is "Done".')
    #
    #     return {
    #         'docs': docs_done,
    #     }