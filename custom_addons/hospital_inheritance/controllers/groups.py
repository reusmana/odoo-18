from odoo import api, models, _

class ResGroups(models.Model):
    _inherit = 'res.groups'


    @api.model
    def get_application_groups(self, domain):
        # Overridden in order to remove 'Show Full Accounting Features' and
        # 'Show Full Accounting Features - Readonly' in the 'res.users' form view to prevent confusion
        group_hospital_doctors = self.env.ref('hospital.group_hospital_doctors')
        if group_hospital_doctors:
            domain += [('id', '!=', group_hospital_doctors.id)]
        return super().get_application_groups(domain)