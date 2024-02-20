from odoo import models, fields, api, exceptions

class Etudiant(models.Model):
    _name = 'education.etudiant'
    _description = 'Modèle des étudiants'
    # _inherit = 'res.users'  # Héritage du modèle res.users

    nom = fields.Char(string='Nom', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    matricule = fields.Char(string='Matricule', required=True, unique=True)
    niveau_id = fields.Many2one(
        comodel_name="education.niveau",
        string="Niveau",
        required=True,
    )
    name = fields.Char(string='Nom complet', compute='_compute_name', store=True)

    

    @api.depends('nom', 'prenom')
    def _compute_name(self):
        for etudiant in self:
            etudiant.name = f"{etudiant.nom} {etudiant.prenom}"

    _sql_constraints = [
        ('unique_matricule', 'unique(matricule)', 'Le matricule de l\'étudiant doit être unique !'),
    ]

    @api.constrains('matricule')
    def _check_unique_matricule(self):
        for etudiant in self:
            existing_student = self.search([('matricule', '=', etudiant.matricule), ('id', '!=', etudiant.id)])
            if existing_student:
                raise exceptions.ValidationError("Le matricule de l'étudiant existe déjà. Veuillez choisir une autre valeur unique.")

