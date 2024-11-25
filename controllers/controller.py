import json
import os

from models import Joueur, Match, Round, Tournoi
from views import Interface

from .tournoi_controller import TournoiController


class Controller:
    """Contrôleur principal de l'application gérant les interactions entre les modèles et les vues."""

    def __init__(self):
        self.interface = Interface(self)
        self.tournoi = None
        self.joueurs = []
        self.matchs = []
        self.rounds = []
        self.tournoi_controller = None
        self.tournois = []
        self.charger_donnees()

    def charger_donnees(self):
        """Charge les données existantes des tournois et joueurs au démarrage."""

        tournois_data = self.charger_tournois()
        self.tournois = tournois_data

        joueurs_data = self.charger_joueurs()
        self.joueurs = joueurs_data

    def charger_tournois(self):
        """Charge les tournois depuis les fichiers JSON et retourne une liste d'objets Tournoi."""
        tournois = []
        if os.path.exists("data/tournaments"):
            for filename in os.listdir("data/tournaments"):
                if filename.endswith(".json"):
                    with open(f"data/tournaments/{filename}", "r") as f:
                        try:  # Convertit les données JSON en un dictionnaire Python
                            data = json.load(f)
                            liste_joueurs = []
                            joueurs_dict = {}
                            # Parcourt la liste des joueurs du tournoi
                            for joueur_data in data.get("liste_joueurs", []):
                                joueur = Joueur(
                                    joueur_data["nom"], joueur_data["prenom"], joueur_data["date_naissance"]
                                )
                                liste_joueurs.append(joueur)
                                joueurs_dict[f"{joueur.nom}_{joueur.prenom}"] = joueur
                            # Crée un objet Tournoi avec les données du fichier JSON
                            tournoi = Tournoi(
                                data["nom"],
                                data["lieu"],
                                data["date_debut"],
                                data["date_fin"],
                                data["nb_tours"],
                                liste_joueurs,
                                data["description"],
                            )
                            # Parcourt la liste des rounds du tournoi
                            if "rounds" in data:
                                for round_data in data["rounds"]:
                                    round = Round(round_data["nom"])
                                    round.date_debut = round_data["date_debut"]
                                    round.date_fin = round_data["date_fin"]
                                    # Parcourt la liste des matchs du round
                                    for match_data in round_data["matchs"]:
                                        try:
                                            joueur1_data = match_data["joueur1"]
                                            joueur2_data = match_data["joueur2"]
                                            joueur1 = joueurs_dict[f"{joueur1_data['nom']}_{joueur1_data['prenom']}"]
                                            joueur2 = joueurs_dict[f"{joueur2_data['nom']}_{joueur2_data['prenom']}"]
                                            # Crée un objet Match avec les données du fichier JSON
                                            match = Match(
                                                joueur1,
                                                joueur2,
                                                match_data.get("score_joueur1", 0),
                                                match_data.get("score_joueur2", 0),
                                            )
                                            round.matchs.append(match)
                                        except (KeyError, TypeError) as e:  # Gère les erreurs de conversion en entier
                                            print(f"Erreur lors du chargement d'un match: {e}")
                                            continue

                                    tournoi.rounds.append(round)

                            tournois.append(tournoi)
                        except json.JSONDecodeError as e:
                            print(f"Erreur lors du chargement du fichier {filename}: {e}")
                            continue  # Passe au tournoi suivant si une erreur est détectée
        return tournois

    def charger_joueurs(self):
        """Charge les joueurs depuis le fichier JSON et retourne une liste d'objets Joueur."""

        joueurs = []
        if os.path.exists("data/joueurs.json"):
            with open("data/joueurs.json", "r") as f:
                try:
                    joueurs_data = json.load(f)
                    for joueur_data in joueurs_data:
                        joueur = Joueur(joueur_data["nom"], joueur_data["prenom"], joueur_data["date_naissance"])
                        joueurs.append(joueur)
                except json.JSONDecodeError:
                    pass  # Passe au joueur suivant si une erreur est détectée
        return joueurs

    def demarrer(self):
        """Lance l'interface principale de l'application."""
        self.interface.menu_principal()

    def nouveau_tournoi(self, nom, lieu, date_debut, date_fin, nb_tours, description):
        """Crée un nouveau tournoi et l'ajoute à la liste des tournois.

        Args:
            nom (str): Nom du tournoi
            lieu (str): Lieu du tournoi
            date_debut (str): Date de début
            date_fin (str): Date de fin
            nb_tours (int): Nombre de tours
            description (str): Description du tournoi
        """

        self.tournoi = Tournoi(nom, lieu, date_debut, date_fin, nb_tours, [], description)
        self.tournois.append(self.tournoi)
        self.tournoi_controller = TournoiController(self.tournoi)
        self.tournoi.sauvegarder()
        return self.tournoi

    def nouveau_joueur(self, nom, prenom, date_naissance):
        """Crée un nouveau joueur et l'ajoute au tournoi actuel s'il existe.

        Args:
            nom (str): Nom du joueur
            prenom (str): Prénom du joueur
            date_naissance (str): Date de naissance
        """
        joueur = Joueur(nom, prenom, date_naissance)
        self.joueurs.append(joueur)
        if self.tournoi:
            self.tournoi.liste_joueurs.append(joueur)
            self.tournoi.sauvegarder()
        joueur.sauvegarder()
        return joueur

    def sauvegarder_tournoi(self):
        """Sauvegarde le tournoi actuel."""
        self.tournoi.sauvegarder()

    def sauvegarder_joueur(self):
        """Sauvegarde tous les joueurs."""
        for joueur in self.joueurs:
            joueur.sauvegarder()

    def charger_tournoi(self, nom):
        """Charge un tournoi spécifique."""
        with open(f"data/tournaments/{nom}.json", "r") as f:
            data = json.load(f)
            return Tournoi(**data)  # Désérialise les données et retourne un objet Tournoi

    def charger_joueur(self, nom):
        """Charge un joueur spécifique."""
        with open("data/joueurs.json", "r") as f:
            data = json.load(f)
            return Joueur(**data)  # Désérialise les données et retourne un objet Joueur

    def get_tournois(self):
        """Retourne tous les tournois."""
        return self.tournois

    def get_joueurs(self):
        """Retourne tous les joueurs."""
        return self.joueurs

    def selectionner_tournoi(self, tournoi):
        """Sélectionne un tournoi et initialise son controller."""
        self.tournoi = tournoi
        self.tournoi_controller = TournoiController(self.tournoi)
        # Si le tournoi a des joueurs, ajoute les joueurs pas encore enregistrés
        if tournoi.liste_joueurs:
            for joueur in tournoi.liste_joueurs:
                if joueur not in self.joueurs:
                    self.joueurs.append(joueur)
