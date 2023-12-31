from odoo import models, fields, api
from datetime import datetime


class support_sys(models.Model):
    _name = 'support_sys.support_sys'
    _description = 'support_sys.support_sys'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    c_id = fields.Integer(string='ID', tracking=True)
    name = fields.Char(string='Client Name', tracking=True)
    image = fields.Binary("Client Image", tracking=True)
    # message = fields.Text(string='Message', required=True)
    issue_description = fields.Char(string='Issued Description', tracking=True)
    support_type = fields.Selection([
        ('ordinary', 'Ordinary'),
        ('vip', 'VIP')
    ], string='Support Type', default='ordinary', help='Select the support type', tracking=True)
    assigned_employee = fields.Char(string='Name of Employee', tracking=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ], string='Status', default='new', tracking=True)
    month_field = fields.Date(
        string='Date',
        widget='Date',
        help='Select a month',
        default=datetime.now().date(), tracking=True
    )
    day_field = fields.Integer(
        string='Day',
        compute='_compute_day_month_year',
        store=True
    )
    months_field = fields.Integer(
        string='Month',
        compute='_compute_day_month_year',
        store=True
    )
    year_field = fields.Integer(
        string='Year',
        compute='_compute_day_month_year',
        store=True
    )

    @api.depends('month_field')
    def _compute_day_month_year(self):
        for record in self:
            record.day_field = record.month_field.day if record.month_field else False
            record.months_field = record.month_field.month if record.month_field else False
            record.year_field = record.month_field.year if record.month_field else False


class Ticket(models.Model):
    _name = 'ticket.raise'
    _description = 'ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string='Name')
    ticket_id = fields.Char(string='Ticket ID')
    ticket_type = fields.Selection(
        [('complain', 'Complain'), ('feedback', 'Feedback'), ('request', 'Request'), ('query', 'Query')],
        string='Ticket Type', tracking=True)
    # employee = fields.Selection([('DeerWalk', 'DeerWalk'), ('Techrida', 'Techrida'), ('TalentConnect', 'TalentConnect'),
    #                              ('TukiLogic', 'TukiLogic'), ('EkSolution', 'EkSolution')],
    #                             string='Employer Of',tracking=True)
    product = fields.Selection([('Internet', 'Internet'), ('Software', 'Software'), ('Website', 'Website')
                                ],
                               string='Choose a Product')
    message = fields.Text(string='Message', required=True)
    priority = fields.Selection([('urgent', 'Urgent'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
                                string='Priority', tracking=True)
    status = fields.Selection(
        [('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Declined', 'Declined')],
        default='New', String="Progress", required=True, tracking=True)
    photo = fields.Binary(string='photo', tracking=True)
    nepalidatepicker = fields.Date(string='Requested date', required=True, tracking=True)
    client_email = fields.Char(string='Client Email', tracking=True)

    # photo_filename = fields.Char(string='photo Filename')

    def action_confirm(self):
        self.write({'status': 'In Progress'})

    def action_decline(self):
        self.write({'status': 'Declined'})

    def action_completed(self):
        self.write({'status': 'Completed'})

    @api.model
    def create(self, vals):
        print("Sequence", vals)
        vals['ticket_id'] = self.env['ir.sequence'].next_by_code("ticket.raise")
        return super(Ticket, self).create(vals)


class Employee(models.Model):
    # _name = 'employee.details'

    _inherit = ['hr.employee']

    employee_id = fields.Char(string='Sequence Number')
    employee_name = fields.Char(string='Employee Name')
   
    _sql_constraints = [
        ('employee_id_uniq', 'unique(employee_id)', 'Employee ID must be unique!'),
    ]

    @api.model
    def create(self, vals):
        print("Sequence", vals)
        vals['employee_id'] = self.env['ir.sequence'].next_by_code("employee.details")
        return super(Employee, self).create(vals)

    class Expense(models.Model):
        _name = 'employee.expense'
        _description = 'employee'
        _inherit = ['mail.thread', 'mail.activity.mixin']
        nepalidatepicker = fields.Date(string='Expense Date', default=fields.Date.today())
        amount = fields.Float(string='Amount', default=None)
        description = fields.Text(string='Description')
        # status = fields.Selection([
        #     ('draft', 'Draft'),
        #     ('submitted', 'Submitted'),
        #     ('approved', 'Approved'),
        #     ('rejected', 'Rejected'),
        # ], string='Status', default='draft',tracking=True)
        expense_category = fields.Selection([
            ('Meals', 'Meals'),
            ('Travel', 'Travel'),
            ('Accomodation', 'Accomodation'),
            ('Other', 'Other'),
        ], string='Expense Category', tracking=True)
        status = fields.Selection(
            [('New', 'New'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
            default='New', String="Progress", required=True, tracking=True)
        starting_location = fields.Char(string='Starting Location', tracking=True)
        ending_location = fields.Char(string='Ending Location', tracking=True)

        photo = fields.Binary("Bill Image", tracking=True)
        hotel_name = fields.Char("H Name")
        hotel_address = fields.Char("H Address",tracking=True)
        hotel_phone = fields.Char("H Contact", tracking=True) 
        def action_accepted(self):
            self.write({'status': 'Accepted'})

        def action_rejected(self):
            self.write({'status': 'Rejected'})

    def submit_ticket(self):
        return {'type': 'ir.actions.act_window_close'}
