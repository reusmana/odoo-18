from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    # this is defedensi mail tracking, one of the feature is tracking changes data
    _inherit = ['mail.thread']
    _description = 'Hospital Patients'

    name = fields.Char(string="Patient Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    age = fields.Char(string="Age", compute='_compute_age', precompute=True)

    tag_ids = fields.Many2many('patient.tag', 'patient_tags_rel', 'patient_id', 'tag_id', string="Tags")

    is_minor = fields.Boolean(string="Is Minor")
    guardian = fields.Char(string="Guardian")
    weight = fields.Float(string="Weight")
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary(string="Image", attachment=True)
    # color = fields.Integer(string="Color Index", default=lambda self: randint(1, 11)) # this is anonym function for get random color
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")

    # this is method override
    # def unlink(self):
    #     # this is for recreate validation error when appointmet have ondelete retrict
    #     for record in self:
    #         domain = [('patient_id', '=', record.id)]
    #         appointment = self.env['hospital.appointment'].search(domain)
    #         if appointment:
    #             raise ValidationError(_('Patient %s has active appointment(s), delete them first.',record.name))
    #     return super(HospitalPatients, self).unlink()


    @api.depends('date_of_birth') # trigger perhitungan ulang when date of birth change
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                dob = record.date_of_birth
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                # ((today.month, today.day) < (dob.month, dob.day)) // this record result boolean between tupple
            else:
                record.age = 0


    # or using ondelete api
    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_appointment(self):
        if any(self.env['hospital.appointment'].search([('patient_id', '=', self.id)])):
            raise ValidationError(_('Patient %s has active appointment(s), delete them first.',self.name))