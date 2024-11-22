import json
import os


class Joueur:
    """Représente un joueur du tournoi."""

    def __init__(self, nom, prenom, date_naissance, score=0):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.score = score

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.score}"

    def to_dict(self):
        """Convertit le joueur en dictionnaire."""
        return {"nom": self.nom, "prenom": self.prenom, "date_naissance": self.date_naissance, "score": self.score}

    def sauvegarder(self):
        """Sauvegarde les données du joueur dans un fichier JSON."""
        if not os.path.exists("data"):
            os.makedirs("data")

        fichier = "data/joueurs.json"
        donnees = self.to_dict()

        joueurs_existants = []
        if os.path.exists(fichier):
            with open(fichier, "r") as f:
                try:
                    joueurs_existants = json.load(f)
                    if not isinstance(joueurs_existants, list):
                        joueurs_existants = [joueurs_existants]
                except json.JSONDecodeError:
                    joueurs_existants = []
        # Recherche si le joueur existe déjà dans la liste
        joueur_existant = next(
            (j for j in joueurs_existants if j["nom"] == self.nom and j["prenom"] == self.prenom), None
        )
        # Met à jour ou ajoute le joueur selon qu'il existe ou non
        if joueur_existant:
            index = joueurs_existants.index(joueur_existant)
            joueurs_existants[index] = donnees
        else:
            joueurs_existants.append(donnees)

        with open(fichier, "w") as f:
            json.dump(joueurs_existants, f, indent=4)
