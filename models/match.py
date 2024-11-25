class Match:
    """Représente un match entre deux joueurs."""

    def __init__(self, joueur1, joueur2, score_joueur1=0, score_joueur2=0):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score_joueur1 = score_joueur1
        self.score_joueur2 = score_joueur2

    def __str__(self):
        joueur1 = f"{self.joueur1.nom} {self.joueur1.prenom} ({self.score_joueur1})"
        joueur2 = f"{self.joueur2.nom} {self.joueur2.prenom} ({self.score_joueur2})"
        return f"{joueur1} vs {joueur2}"

    def resultat_match(self, resultat):
        """Enregistre le résultat du match et met à jour les scores des joueurs.

        Args:
            resultat (str): '1' pour victoire joueur1, '2' pour victoire joueur2, '0' pour match nul
        """
        if resultat not in ["0", "1", "2"]:
            raise ValueError("Résultat invalide")
        if resultat == "1":
            self.joueur1.score += 1
            self.score_joueur1 = 1
            self.score_joueur2 = 0
        elif resultat == "2":
            self.joueur2.score += 1
            self.score_joueur1 = 0
            self.score_joueur2 = 1
        elif resultat == "0":
            self.joueur1.score += 0.5
            self.joueur2.score += 0.5
            self.score_joueur1 = 0.5
            self.score_joueur2 = 0.5

    def to_dict(self):
        """Convertit le match en dictionnaire pour la sérialisation JSON."""
        return {
            "joueur1": self.joueur1.to_dict(),
            "joueur2": self.joueur2.to_dict(),
            "score_joueur1": self.score_joueur1,
            "score_joueur2": self.score_joueur2,
        }

    @property
    def joueurs(self):
        """Propriété qui retourne la liste des deux joueurs du match.
        Permet d'accéder aux joueurs comme un attribut: match.joueurs
        au lieu d'une méthode: match.joueurs()"""
        return [self.joueur1, self.joueur2]
