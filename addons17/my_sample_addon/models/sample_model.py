from odoo import models, fields, api

class SampleModel(models.Model):
    _name = 'sample.model'
    _description = 'Sample Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    
    @api.model
    def create(self, vals):
        return super(SampleModel, self).create(vals)
