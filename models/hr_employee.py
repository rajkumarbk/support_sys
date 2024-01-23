from odoo import api, models, fields


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    Title = fields.Char("Title", readonly=True)
    Ticket_num = fields.Char("Ticket Number", readonly=True)
    e_priority = fields.Char("Priority", readonly=True)
    problem = fields.Char("Problem Description", readonly=True)
    e_image=fields.Binary(string="photo",readonly=True)