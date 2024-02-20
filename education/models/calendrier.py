from odoo import models, fields, api, _, exceptions


class Calendrier(models.Model):
    _name = "education.calendar"
    _description = "Calendrier des cours"

    date_debut = fields.Datetime(string="Date de début")  # Utilisez DateTime pour inclure l'heure
    date_fin = fields.Datetime(string="Date de fin")  
    enseignant_ids = fields.Many2one(
        comodel_name="res.users",
        string="Enseignant",
    )
    niveau_id = fields.Many2one(
        comodel_name="education.niveau",
        string="Niveau",
        required=True,
    )
    classe_ids = fields.Many2one(
        comodel_name="education.classes",
        string="Classe",
        required=True,
    )
    cours_ids = fields.Many2one(
        comodel_name="education.cours",
        string="Cours",
    )
    statut = fields.Selection([
        ("pas démarré", "Pas démarré"),
        ("en cours", "En cours"),
        ("terminé", "Terminé"),
    ], string="Statut")


    user_id = fields.Many2one(string='User', comodel_name='res.users', default=lambda self: self.env.user)
    niv_final= fields.Many2one(comodel_name ='education.niveau', compute= '_get_niveau' )

    name = fields.Char(string='Code', default=lambda self: _('New'), readonly=True)
    @api.model
    def create(self, vals):
        
        
        if vals.get('name', _('New')) == _('New'):
            # Utilisation de la séquence pour générer le champ 'name'
            vals['name'] = self.env['ir.sequence'].next_by_code('education.calendar') or _('New')

        return super(Calendrier, self).create(vals)
    
    @api.onchange("date_debut")
    def onchange_date_debut(self):
        # Vérifier si la date de début est postérieure ou égale à la date actuelle
        if self.date_debut and self.date_debut < fields.Datetime.now():
            raise exceptions.ValidationError(_("La date de début que vous choisissez est déjà passée. Veuillez choisir une date à partir d'aujourd'hui."))

    
    # @api.model
    # def _search_filter_my_courses(self, operator, value):
    #     user = self.env.user
    #     return [('niveau_id', '=', user.niveau_id)]

    # _search = [
    #     ('filter_my_courses', _search_filter_my_courses),
    # ]

    @api.depends('user_id')
    def _get_niveau(self):
        self.niv_final = self.env['res.users'].browse(self.user_id.id).niveau_id.id