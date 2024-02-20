# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Enseignant(models.Model):
    """
    Modèle représentant un enseignant.
    """
    _name = "education.enseignant"
    _description = "Enseignant"

    name = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    tel = fields.Char(string="Téléphone")
    grade = fields.Selection([
                    ("Docteur", "Docteur"),
                    ("Professeur", "Professeur"),
                    ("Maître de conférence", "Maître de conférence"),
                    ("Chargé de cours", "Chargé de cours"),
                ], string="Grade", required=True)
    # niveau_id = fields.Many2many(
    #     comodel_name="education.niveau",
    #     string="Niveau",
    #     required=True,
    # )
    cours_ids = fields.Many2many(
        comodel_name="education.cours",
        string="Liste des cours",
    )
    @api.onchange('niveau_id')
    def onchange_niveau_id(self):
        if self.niveau_id:
            # Filtrer les cours en fonction du niveau sélectionné
            cours_domain = [('id', 'in', self.niveau_id.cours_ids.ids)]
            return {'domain': {'cours_ids': cours_domain}}

    