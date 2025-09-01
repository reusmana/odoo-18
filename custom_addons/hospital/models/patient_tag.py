from odoo import models, fields, api, _

class PatientTags(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tags'
    _order = 'sequence, id' # this order for display
    _rec_name = 'name' #this is for the name of the record

    name = fields.Char(string="Name", required=True)

    sequence = fields.Integer(string="Sequence", default=10) # need sequence for reorder list
    color = fields.Integer(string="Color", copy=1) # whne is duplicate the tag, copy id default 1

    # _sql_constraints = [('name_uniq', "unique(name, applicability, country_id)", "A tag with the same name and applicability already exists in this country.")]
    _sql_constraints = [('name_uniq', "unique(name)", "A tag name with the same name already exists in this tags."), (
        'check_sequence', 'CHECK(sequence > 0)', 'The sequence number must be strictly positive.'
    )]


    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        """ Override Name tag when duplicate the record. """
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        return  super(PatientTags, self).copy(default)