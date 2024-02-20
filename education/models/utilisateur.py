from odoo import models, fields, api, exceptions

class Utilisateurs(models.Model):
    #  _name = 'education.utilisateurs'
    _inherit = 'res.users'  # Héritage du modèle res.users

  
    matricule = fields.Char(string='Matricule', unique=True)
    type_utilisateur = fields.Selection([
                                ('enseignant', 'enseignant'),
                                ('etudiant', 'etudiant'),
                            ], string='Type d\'utilisateur', required=True)

    niveau_id = fields.Many2one(
        comodel_name="education.niveau",
        string="Niveau",
    )

    tel = fields.Char(string="Téléphone")
    grade = fields.Selection([
                    ("Docteur", "Docteur"),
                    ("Professeur", "Professeur"),
                    ("Maître de conférence", "Maître de conférence"),
                    ("Chargé de cours", "Chargé de cours"),
                ], string="Grade")
    
    cours_ids = fields.Many2many(
        comodel_name="education.cours",
        string="Liste des cours",
    )


    # Ajouter le décorateur onchange pour gérer la visibilité des champs
    @api.onchange('type_utilisateur')
    def onchange_type_utilisateur(self):
        if self.type_utilisateur == 'enseignant':
             # Si l'utilisateur est un enseignant, rendre les champs matricule et niveau_id invisibles, les autres visibles
            return {'value': {'matricule': False, 'niveau_id': False, 'tel': False, 'grade': 'Docteur', 'cours_ids': False}}
        elif self.type_utilisateur == 'etudiant':
            # Si l'utilisateur est un étudiant, rendre les champs matricule et niveau_id visibles, les autres invisibles
            return {'value': {'matricule': False, 'niveau_id': True, 'tel': False, 'grade': False, 'cours_ids': False}}

        else:
            # Si le type n'est ni enseignant ni étudiant, rendre tous les champs invisibles
            return {'value': {'matricule': False, 'niveau_id': False, 'tel': False, 'grade': False, 'cours_ids': False}}
    

    _sql_constraints = [
        ('unique_matricule', 'unique(matricule)', 'Le matricule de l\'étudiant doit être unique !'),
    ]

    # @api.constrains('matricule')
    # def _check_unique_matricule(self):
    #     for etudiant in self:
    #         existing_student = self.search([('matricule', '=', etudiant.matricule), ('id', '!=', etudiant.id)])
    #         if existing_student:
    #             raise exceptions.ValidationError("Le matricule de l'étudiant existe déjà. Veuillez choisir une autre valeur unique.")