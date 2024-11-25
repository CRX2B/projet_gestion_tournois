import json
import os


class Tournoi:
    """Gère un tournoi d'échecs et ses données."""

    def __init__(self, nom, lieu, date_debut, date_fin, nb_tours, liste_joueurs, description):
        """Initialise un nouveau tournoi."""
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tours = nb_tours
        self.liste_joueurs = liste_joueurs
        self.description = description
        self.rounds = []

    def __str__(self):
        """Retourne la représentation textuelle du tournoi."""
        return (
            f"Tournoi: {self.nom}\n"
            f"Lieu: {self.lieu}\n"
            f"Dates: {self.date_debut} - {self.date_fin}\n"
            f"Tours: {self.nb_tours}\n"
            f"Joueurs: {self.liste_joueurs}\n"
            f"Description: {self.description}"
        )

    def to_dict(self):
        """Convertit le tournoi en dictionnaire pour la sérialisation JSON."""
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nb_tours": self.nb_tours,
            "liste_joueurs": [joueur.to_dict() for joueur in self.liste_joueurs],
            "description": self.description,
            "rounds": [round.to_dict() for round in self.rounds],
        }

    def sauvegarder(self):
        """Sauvegarde les données du tournoi dans un fichier JSON."""
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")

        fichier = f"data/tournaments/{self.nom}.json"
        donnees = self.to_dict()

        with open(fichier, "w") as f:
            json.dump(donnees, f, indent=4)
