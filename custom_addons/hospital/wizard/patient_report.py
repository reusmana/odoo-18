from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


# TransientModel is for wizard, its not store to db
class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'Patient Report Wizard'

    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", required=True, default=fields.Date.context_today)

    def action_print_report(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start Date cannot be greater than End Date.")
        
        docs = self.env['hospital.patients'].search([('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])
        if not docs:
            raise ValidationError("No patients found for the specified date range.")
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'docs': docs,
        }
        print("----data", data)
        return self.env.ref('hospital.action_report_hospital_patient_wizard').report_action(self, data=data)
    

class ReportPatientWizard(models.AbstractModel):
    _name = 'report.hospital.report_patients_name'
    _description = 'Patient Report Wizard Data'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(docids)
        docs = data.get('docs', self.env['hospital.patients'].browse(docids))

        print("----data in report", docs)
        return {
            'doc_ids': docids,
            'doc_model': 'hospital.patients',
            'data': data,  # <- ini supaya kamu bisa akses data di template
            'docs': docs,
        }