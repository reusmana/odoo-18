from odoo import models, fields, api
from datetime import datetime

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.now()
        print("sss--------------------", self.env.context)
        res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason")
    date_cancel = fields.Datetime(string="Date Cancel")

    


    def action_cancel_appointment_func(self):
        print("sini")
        self.appointment_id.action_cancel()
        return