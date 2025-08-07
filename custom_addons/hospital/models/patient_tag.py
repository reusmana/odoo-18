from odoo import models, fields, api

class PatientTags(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tags'
    _order = 'sequence, id' # this order for display
    _rec_name = 'name' #this is for the name of the record

    name = fields.Char(string="Name", required=True)

    sequence = fields.Integer(string="Sequence", default=10)