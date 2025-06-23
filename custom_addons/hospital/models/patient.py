from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatients(models.Model):
    _name = 'hospital.patients'
    # this is defedensi mail tracking, one of the feature is tracking changes data
    _inherit = ['mail.thread']
    _description = 'Hospital Patients'

    name = fields.Char(string="Patient Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")

    tag_ids = fields.Many2many('patient.tag', 'patient_tags_rel', 'patient_id', 'tag_id', string="Tags")

    is_minor = fields.Boolean(string="Is Minor")
    guardian = fields.Char(string="Guardian")
    weight = fields.Float(string="Weight")

    # this is method override
    # def unlink(self):
    #     # this is for recreate validation error when appointmet have ondelete retrict
    #     for record in self:
    #         domain = [('patient_id', '=', record.id)]
    #         appointment = self.env['hospital.appointment'].search(domain)
    #         if appointment:
    #             raise ValidationError(_('Patient %s has active appointment(s), delete them first.',record.name))
    #     return super(HospitalPatients, self).unlink()


    # or using ondelete api
    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_appointment(self):
        if any(self.env['hospital.appointment'].search([('patient_id', '=', self.id)])):
            raise ValidationError(_('Patient %s has active appointment(s), delete them first.',self.name))