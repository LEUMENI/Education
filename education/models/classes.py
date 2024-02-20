from odoo import models, fields, api



class EducationClasse(models.Model):
    _name = 'education.classes'
    _description = 'Modèle pour représenter les classes'

    nom_batiment =fields.Char(string='Nom du batiment')
    number = fields.Integer(string='Numéro de la salle', default=False )
    capacite = fields.Integer(string='Capacité de la Classe', default=False)
    # niveau_id = fields.Many2one('education.niveau', string='Niveau')
    nom = fields.Char(string='Nom de la Classe', required=True, compute='_compute_nom')

    @api.depends('number', 'nom_batiment')
    def _compute_nom(self):
        for record in self:
            record.nom = f"{record.number or ''}{record.nom_batiment or ''}"
    name = fields.Char(string="Number/nom_batiment", compute="_compute_name")

    @api.depends("number", "nom_batiment")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.number}{record.nom_batiment}"



    _sql_constraints = [
        ('positive_capacite', 'check(capacite > 0)', 'La capacité doit être un nombre positif !'),
    ]

    