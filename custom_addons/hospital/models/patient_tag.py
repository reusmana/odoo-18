from odoo import models, fields, api

class PatientTags(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tags'
    _order = 'sequence, id'

    name = fields.Char(string="Name", required=True)

    sequence = fields.Integer(string="Sequence", default=10)