from email.policy import default

from odoo import models, fields, api

class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _rec_name = 'operation_name'

    _log_access = False

    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Operation Name")

    # like many2one but
    # Tidak ada relasi langsung ke SQL foreign key (beda dengan Many2one yang punya constraint DB).
    # Tidak bisa pakai ondelete behavior (cascade, restrict, dll).
    # Agak susah kalau mau pakai domain filtering kompleks.
    records = fields.Reference(selection=[('hospital.patients', 'Patient'), ('hospital.appointment', 'Appointment') ], string="Records")

    @api.model
    def name_create(self, name):
        """ for create name of operation via many 2 one selecttion, 
        if example you can see on appointment and select operation, then create
        """
        name = self.create({'operation_name': name})
        return name.display_name