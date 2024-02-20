from odoo import models, fields, api, exceptions

class Cours(models.Model):
    _name = 'education.cours'
    _description = 'Modèle des cours'

    titre = fields.Char(string='Titre', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')

    enseignant_id = fields.Many2many(
        comodel_name="res.users",
        string="Enseignant",
        required=True,
    )
    niveau_ids = fields.Many2many('education.niveau', string='Niveaux associés', help="Liste des niveaux associés à ce cours")
    name = fields.Char(string="Titre - Code", compute="_compute_name")
    

    @api.depends("titre", "code")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.titre} - {record.code}"

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Le code du cours doit être unique !'),
    ]

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            existing_course = self.search([('code', '=', record.code), ('id', '!=', record.id)])
            if existing_course:
                raise exceptions.ValidationError("Le code du cours doit être unique !")
