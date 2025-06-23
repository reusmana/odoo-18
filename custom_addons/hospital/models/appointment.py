from email.policy import default

from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    # this is defedensi mail tracking, one of the feature is tracking changes data
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id' #this is for the name of the record
    _rec_names_search = ['reference', 'patient_id']

    # create squecnce ref
    reference = fields.Char(string="Reference", default='new')
    # ondelete restrict is when record patien is delete, but patient id has record on appointment, is get the error
    # but if you want delete record patient and appoiintment delete also, you can use ondelete='cascade'
    # but if you want delete record patient then apointment on field patient_id set null, u can use ondelete='set null'
    patient_id = fields.Many2one('hospital.patients', string="Patient", tracking=True, required=False, ondelete='restrict')
    date_appointment = fields.Datetime(string="Date of Appointment", tracking=True)
    note = fields.Text(string="Note", tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'), ('cancel', 'Cancel')], string="Status", default='draft', tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string="Appointment Lines")

    # this total_qty not store to db, but when want to store to db, just addtional attribute
    # like store=True
    total_qty = fields.Float(string="Total Quantity", compute='_compute_total_qty', store=True, precompute=True)

    # this colum for related field dob from patient_id, not store to db
    date_of_birth = fields.Date(related='patient_id.date_of_birth' , groups="hospital.group_hospital_doctors")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'new') == 'new':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or '/'
        return super(HospitalAppointment, self).create(vals_list)

    # show name and ref when relation this class, want to get ref and name
    @api.depends('patient_id', 'reference')
    def _compute_display_name(self):
        for cr in self:
            cr.display_name = f"[{cr.reference}] {cr.patient_id.name}"

    # thiis is api.depent need for recompute field
    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        total_qty = 0.0
        for line in self.appointment_line_ids:
            total_qty += line.qty
        self.total_qty = total_qty
        # self.total_qty = sum(self.appointment_line_ids.mapped('qty'))

    def action_confirm(self):
        self.state = 'confirmed'
        # self.write({'state': 'confirmed'})

    def action_ongoing(self):
        self.state = 'ongoing'
        # self.write({'state': 'ongoing'})

    def action_done(self):
        self.state = 'done'
        # self.write({'state': 'done'})

    def action_cancel(self):
        self.state = 'cancel'
        # self.write({'state': 'cancel'})


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string="Quantity")