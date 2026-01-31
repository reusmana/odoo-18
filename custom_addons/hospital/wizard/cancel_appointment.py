from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from datetime import date, datetime, timedelta

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.now()
        print("sss--------------------", self.env.context)
        # self.env.context.get('active_id') itu memang bawaan Odoo.
        # Dia otomatis diisi sama framework Odoo ketika kamu buka action (misalnya klik button, atau pilih record lalu klik action).
        # Mekanismenya
        # Kalau kamu buka wizard lewat tombol action di tree/form view, Odoo akan kirim context ke wizard.
        # Di dalam context, Odoo biasanya tambahkan:
        # active_id → ID record yang sedang aktif (hanya satu record).
        # active_ids → daftar ID kalau kamu pilih banyak record.
        # active_model → nama model sumber (misalnya 'hospital.appointment').
        res['appointment_id'] = self.env.context.get('active_id')
        return res

    # filter appointment by domain state
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", domain=[('state', '=', 'draft')])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Datetime(string="Date Cancel")

    


    def action_cancel_appointment_func(self):
        print("sini")
        get_cancel = self.env['ir.config_parameter'].sudo().get_param('hospital.cancel_days')
        allow_cancel = self.appointment_id.date_appointment - relativedelta(days=int(get_cancel))
        print(self.appointment_id.date_appointment)
        print("shinnn")
        print(allow_cancel)
        print(datetime.today())
        if allow_cancel < datetime.today():
            raise ValidationError("You can't cancel the appointment, you can only cancel the appointment %s days before the appointment date." % get_cancel)
        
        self.appointment_id.action_cancel()
        # for reload when cancel appointment is updated
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}