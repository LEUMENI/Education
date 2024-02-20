# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, exceptions
 

class Coordination(models.Model):
    """
    Modèle représentant une coordination.
    """
    _name = "education.coordination"
    _description = "Coordination"

    enseignant_ids = fields.Many2one(
        comodel_name="res.users",
        string="Enseignant",
        required=True,
        domain="[('type_utilisateur', '=', 'enseignant')]",
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

    date_debut = fields.Datetime(string="Date de début", required=True)
    date_fin = fields.Datetime(string="Date de fin",required=True )
    statut = fields.Selection([
        ("pas démarré", "Pas démarré"),
        ("en cours", "En cours"),
        ("terminé", "Terminé"),
    ], string="Statut")

    calendrier_id = fields.Many2one('education.calendar', string="Calendrier associé")
    name = fields.Char(string='Code', default=lambda self: _('New'), readonly=True)
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            # Utilisation de la séquence pour générer le champ 'name'
            vals['name'] = self.env['ir.sequence'].next_by_code('education.coordination') or _('New')

        return super(Coordination, self).create(vals)

    # @api.onchange("date_fin")
    # def onchange_date_fin(self):
    #     if self.date_debut == self.date_fin:
    #         self.statut = "terminé"
    
   
   
    # @api.onchange("enseignant_id")
    # def onchange_enseignant_id(self):
    #     """
    #     Mettez à jour les programmations en fonction de l'enseignant sélectionné.
    #     """
    #     if self.enseignant_id:
    #         # Récupérer la liste des programmations de l'enseignant
    #         programmations = self.env['education.programmation'].search([('enseignant_id', '=', self.enseignant_id.id)])
    #         self.programmations_ids = [(6, 0, programmations.ids)]

    @api.model
    def create(self, vals):
        coordination = super(Coordination, self).create(vals)

        # Créer automatiquement le calendrier associé
        calendrier_vals = {
            'enseignant_ids': coordination.enseignant_ids.id,
            'classe_ids': coordination.classe_ids.id,
            'cours_ids': coordination.cours_ids.id,
            'date_debut': coordination.date_debut,
            'date_fin': coordination.date_fin,
            'statut': coordination.statut,
            'coordination_id': coordination.id,
            'niveau_id':coordination.niveau_id.id,
        }
        self.env['education.calendar'].create(calendrier_vals)

        return coordination


    @api.onchange("date_debut")
    def onchange_date_debut(self):
        # Vérifier si la date de début est postérieure ou égale à la date actuelle
        if self.date_debut and self.date_debut < fields.Datetime.now():
            raise exceptions.ValidationError(_("La date de début que vous choisissez est déjà passée. Veuillez choisir une date à partir d'aujourd'hui."))
    
    @api.onchange("date_fin")
    def onchange_date_fin(self):
        if self.date_debut and self.date_fin and self.date_debut > self.date_fin:
            raise exceptions.ValidationError(_("La date de fin doit être supérieure à la date de début."))
    

    @api.constrains('niveau_id', 'classe_id')
    def _check_capacity(self):
        for record in self:
            if record.niveau_id and record.classe_ids:
                if record.niveau_id.nombre_etudiants > record.classe_ids.capacite:
                    raise exceptions.ValidationError("Vous ne pouvez pas programmer ce cours dans cette classe car le nombre de places est insuffisant pour ce niveau.")

    
   