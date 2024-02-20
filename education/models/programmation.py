# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Programmation(models.Model):
    _name = "education.programmation"
    _description = "Programmation"

    enseignant_id = fields.Many2one(
        comodel_name="education.enseignant",
        string="Enseignant",
    )
    cours_id = fields.Many2one(
        comodel_name="education.cours",
        string="Cours",
    )
    classe_id = fields.Many2one(
        comodel_name="education.classe",
        string="Classe",
    )
    date_debut = fields.Date(string="Date de début")
    date_fin = fields.Date(string="Date de fin")

    