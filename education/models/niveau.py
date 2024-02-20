from odoo import models, fields, api

class Niveau(models.Model):
    _name = 'education.niveau'
    _description = 'Modèle pour représenter les niveaux académiques'

    nom = fields.Integer(string='Nom du Niveau', required=True)
    nombre_etudiants = fields.Integer(string='Nombre d\'étudiants')
    departement = fields.Selection([
        ("Génie Civil", "Génie Civil"),
        ("Génie Mécanique", "Génie Mécanique"),
        ("Génie Electrique", "Génie Electrique"),
        ("Génie Informatique", "Génie Informatique"),
        ("Génie Chimique", "Génie Chimique"),
        ("Génie Des Matériaux", "Génie Des Matériaux"),
        ("Génie Nucléaire", "Génie Nucléaire"),
        ("Génie Des Télécommunication", "Génie Des Télécommunication"),
    ], string="Département")

    name = fields.Char(string="departement/nom", compute="_compute_name")

    @api.depends("departement", "nom")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.departement}{record.nom}"

    cours_ids = fields.Many2many('education.cours', string='Cours associés', help="Liste des cours associés à ce niveau")
 
    _sql_constraints = [
        #  ('unique_nom_departement', 'unique(nom, departement)', 'Le niveau existe déjà pour ce département. Veuillez choisir un autre nom !'),
        ('positive_nombre_etudiants', 'check( nombre_etudiants  > 0)', 'La  nombre d\'étudiants  doit être un nombre positif !'),
    ]
   
   
