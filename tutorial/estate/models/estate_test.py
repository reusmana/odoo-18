from odoo import models, fields, api

class EstateTest(models.Model):
    _name = 'estate.test'
    _description = 'Estate Test'

    name = fields.Char(required=True, string="Name", help="Name Tooltips", index=True)
    description = fields.Text( string="Description")
    postcode = fields.Char( string="Postcode")
    date_availability = fields.Date( string="Date Availability")
    expected_price = fields.Float( string="Expected Price")
    selling_price = fields.Float( string="Selling Price")
    bedrooms = fields.Integer( string="Bedrooms")
    living_area = fields.Integer( string="Living Area")
    facades = fields.Integer( string="Facades")
    garage = fields.Boolean( string="Garage")
    garden = fields.Boolean( string="Garden")
    garden_area = fields.Integer( string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string="Garden Orientation")
    active = fields.Boolean( string="Active", default=True)