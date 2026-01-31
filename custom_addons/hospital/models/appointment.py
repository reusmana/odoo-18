from email.policy import default

from odoo import models, fields, api, _

from odoo.exceptions import UserError, ValidationError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    # this is defedensi mail tracking, one of the feature is tracking changes data
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id' #this is for the name of the record
    _rec_names_search = ['reference', 'patient_id']

    # create squecnce ref
    reference = fields.Char(string="Reference", default='new')
    # ondelete restrict is when record patien is delete, but patient id has record on appointment, is get the error
    # but if you want delete record patient and appoiintment delete also, you can use ondelete='cascade'
    # but if you want delete record patient then apointment on field patient_id set null, u can use ondelete='set null'
    patient_id = fields.Many2one('hospital.patients', string="Patient", tracking=True, required=False, ondelete='restrict')
    date_appointment = fields.Datetime(string="Date of Appointment", tracking=True, default=fields.Datetime.now)
    note = fields.Text(string="Note", tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'), ('cancel', 'Cancel')], string="Status", default='draft', tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string="Appointment Lines")

    # this total_qty not store to db, but when want to store to db, just addtional attribute
    # like store=True
    total_qty = fields.Float(string="Total Quantity", compute='_compute_total_qty', store=True, precompute=True)

    doctor_ids = fields.Many2one('res.users', string="Doctor")

    # this colum for related field dob from patient_id, not store to db
    date_of_birth = fields.Date(related='patient_id.date_of_birth' , groups="hospital.group_hospital_doctors") # its field is automtic show gender when select patient_id
    # group is for security, it mean just this group can see this field or user can this view

    description = fields.Html(string="Description") # this is for text rich

    # 
    priority = fields.Selection([('0', 'Low'), ('1', 'Medium'), ('2', 'High')], string="Priority", default='0')

    hide_and_seek = fields.Boolean(string="Hide and Seek")

    operation_id = fields.Many2one('hospital.operation', string="Operation")

    progress = fields.Integer(string="Progress", compute='_compute_progress')

    progress_gauge = fields.Float(string="Progress Gauge", compute='_compute_progress')

    duration = fields.Float(string="Duration")

    # this is for current company
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    price_subtotal = fields.Monetary(string="Subtotal", related='appointment_line_ids.price_subtotal')

    total = fields.Monetary(string="Total", compute='_compute_total', precompute=True)

    @api.depends('appointment_line_ids.price_subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = sum(line.price_subtotal for line in rec.appointment_line_ids)

    def action_open_form(self):
        print("open form bro")
        print(self.id)
        print(self.patient_id.id)
        # {
        #     "type": "ir.actions.act_window",
        #     "res_model": "product.product",
        #     "views": [[False, "form"]],
        #     "res_id": a_product_id,
        #     "target": "new",
        # }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patients',
            # open form view 
            "views": [[False, "form"]], 
            # 'view_mode': 'form',
            # open form view hospital.patients with this id
            'res_id': self.patient_id.id,
            'target': 'new',  # Open in a new window
        }
    
    def open_custom_widget(self):
        print("open custom widget bro")
        return {
            'type': 'ir.actions.client',
            'tag': 'my_widget_action',
            'params': {
                'env': 'info',
                'action': 'hohohoo',
            },
        }

   

    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = 25
                rec.progress_gauge = 25
            elif rec.state == 'confirmed':
                rec.progress = 50
                rec.progress_gauge = 50
            elif rec.state == 'ongoing':
                rec.progress = 75
                rec.progress_gauge = 75
            elif rec.state == 'done':
                rec.progress = 100
                rec.progress_gauge = 100
            elif rec.state == 'cancel':
                rec.progress = 0
                rec.progress_gauge = 0

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

    # def name_get(self):
    #     return [(rec.id, "%s %s" % (rec.reference, rec.patient_id.name)) for rec in self]

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
        print("cancel bro")
        # action = self.env.ref('hospital.action_cancel_appointment')
        # return action.read()[0]
        self.state = 'cancel'
        # self.write({'state': 'cancel'})

    def testing_clicking(self):

        # if wannna redirect to url 
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': 'https://google.com',
        #     'target': 'new',
        # }
    
        return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "you are click this button",
                    # 'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        return True
    
    def action_share_wa(self):
        print("whatsapp")

        self.message_post(body=_("share to whatsapp"), subject='whatapps')

        if self.patient_id.phone:
            return {
                'type': 'ir.actions.act_url',
                'url': 'https://wa.me/62%s' % self.patient_id.phone,
                'target': 'new',
            }
        
        raise ValidationError(_("Phone number not found with number %s",  self.patient_id.phone))
    

    def check_notify(self):
        print("check notify")
        # success, warning, danger 
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'sticky': False,
                'message': _("Accounts successfully merged!"),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        return


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    # ondelete='cascade' its mean, when patient delete from patien, this record also delete,
    # ondelete='set null' its mean, when patient delete from patien, this record also set null
    # ondelete='restrict' its mean, when patient delete from patien, this record not delete, and the patient to have message error
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_sale_unit = fields.Float(related='product_id.list_price', readonly=True, digits='Product Price') # digit on menu setting decimal according to currency
    qty = fields.Float(string="Quantity")

    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string="Subtotal", store=True, compute='_compute_amounts')

    @api.depends('product_id', 'qty')
    def _compute_amounts(self):
        for line in self:
            line.price_subtotal = line.product_sale_unit * line.qty