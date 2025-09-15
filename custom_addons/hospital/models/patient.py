from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from datetime import date, datetime, timedelta


class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    # this is defedensi mail tracking, one of the feature is tracking changes data
    _inherit = ['mail.thread']
    _description = 'Hospital Patients'


    # log access, if false make remove create_date, create_uid, write_date, write_uid on table
    # _log_access = False

    name = fields.Char(string="Patient Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")

    # inverse can editabel age
    age = fields.Integer(string="Age", compute='_compute_age', inverse="_inverse_age", search='_search_age', precompute=True)

    tag_ids = fields.Many2many('patient.tag', 'patient_tags_rel', 'patient_id', 'tag_id', string="Tags")

    is_minor = fields.Boolean(string="Is Minor")
    guardian = fields.Char(string="Guardian")
    weight = fields.Float(string="Weight")
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary(string="Image", attachment=True)
    # color = fields.Integer(string="Color Index", default=lambda self: randint(1, 11)) # this is anonym function for get random color
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")

    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital Status")
    partner_name = fields.Char(string="Partner Name")
    is_birth = fields.Boolean(string="Is Birth", compute='_compute_is_birth')

    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)

    # this is method override
    # def unlink(self):
    #     # this is for recreate validation error when appointmet have ondelete retrict
    #     for record in self:
    #         domain = [('patient_id', '=', record.id)]
    #         appointment = self.env['hospital.appointment'].search(domain)
    #         if appointment:
    #             raise ValidationError(_('Patient %s has active appointment(s), delete them first.',record.name))
    #     return super(HospitalPatients, self).unlink()

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for record in self:
            domain = [('patient_id', '=', record.id)]
            record.appointment_count = self.env['hospital.appointment'].search_count(domain)

    @api.depends('date_of_birth')
    def _compute_is_birth(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                dob = record.date_of_birth
                record.is_birth = ((today.month, today.day) < (dob.month, dob.day))
            else:
                record.is_birth = False


    @api.constrains('date_of_birth') #validation date
    def _check_date_of_birth(self):
        for patient in self:
            if patient.date_of_birth > date.today():
                raise ValidationError(_('You cannot set a date of birth in the future. (date of birth: %s)', patient.date_of_birth))
            
    @api.constrains('age')
    def _inverse_age(self):
        today = date.today()
        for patient in self:
            if patient.age:
                patient.date_of_birth = today - relativedelta(years=int(patient.age))


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
        

    # searchable function for non store to db in field model,
    # like age, because age not store in database
    def _search_age(self, operator, value):
        """Allow searching by age"""
        today = date.today()
        try:
            value = int(value)
        except ValueError:
            return []

        # Hitung tanggal lahir yang sesuai dengan umur
        start_date = today.replace(year=today.year - value - 1) + timedelta(days=1)
        end_date = today.replace(year=today.year - value)

        print(start_date)
        print(end_date)

        return [('date_of_birth', '>=', start_date), ('date_of_birth', '<=', end_date)]
    
    def action_view_appointment_count(self):
        self.ensure_one() # this is for only one record, this is for one2many
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hospital Appointments'),
            'res_model': 'hospital.appointment',
            'views': [[False, 'list'], [False, 'form'], [False, 'calendar']],
            'context': {'default_patient_id': self.id}, # this is for add record appointment, the name is default patient
            'domain': [('id', 'in', self.appointment_ids.ids)],
        }
    
    # @api.multi
    def _test_cron_job(self):
        print('test cron job')