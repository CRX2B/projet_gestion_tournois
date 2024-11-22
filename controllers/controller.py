import json
import os

from views import Interface
from models import Tournoi, Joueur, Match, Round
from .tournoi_controller import Tournoi_Controller


class Controller:
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
        """Charge les données existantes au démarrage"""
        # Charger les tournois
        tournois_data = self.charger_tournois()
        self.tournois = tournois_data
        
        # Charger les joueurs
        joueurs_data = self.charger_joueurs()
        self.joueurs = joueurs_data
        
    def charger_tournois(self):
        tournois = []
        if os.path.exists("data/tournaments"):
            for filename in os.listdir("data/tournaments"):
                if filename.endswith(".json"):
                    with open(f"data/tournaments/{filename}", "r") as f:
                        try:
                            data = json.load(f)
                            liste_joueurs = []
                            joueurs_dict = {}
                            
                            for joueur_data in data.get("liste_joueurs", []):
                                joueur = Joueur(
                                    joueur_data["nom"],
                                    joueur_data["prenom"],
                                    joueur_data["date_naissance"]
                                )
                                liste_joueurs.append(joueur)
                                joueurs_dict[f"{joueur.nom}_{joueur.prenom}"] = joueur
                                
                            tournoi = Tournoi(
                                data["nom"],
                                data["lieu"],
                                data["date_debut"],
                                data["date_fin"],
                                data["nb_tours"],
                                liste_joueurs,
                                data["description"]
                            )
                            
                            if "rounds" in data:
                                for round_data in data["rounds"]:
                                    round = Round(round_data["nom"])
                                    round.date_debut = round_data["date_debut"]
                                    round.date_fin = round_data["date_fin"]
                                    
                                    for match_data in round_data["matchs"]:
                                        try:
                                            joueur1_data = match_data["joueur1"]
                                            joueur2_data = match_data["joueur2"]
                                            joueur1 = joueurs_dict[f"{joueur1_data['nom']}_{joueur1_data['prenom']}"]
                                            joueur2 = joueurs_dict[f"{joueur2_data['nom']}_{joueur2_data['prenom']}"]
                                            
                                            match = Match(
                                                joueur1,
                                                joueur2,
                                                match_data.get("score_joueur1", 0),
                                                match_data.get("score_joueur2", 0)
                                            )
                                            round.matchs.append(match)
                                        except (KeyError, TypeError) as e:
                                            print(f"Erreur lors du chargement d'un match: {e}")
                                            continue
                                        
                                    tournoi.rounds.append(round)
                                    
                            tournois.append(tournoi)
                        except json.JSONDecodeError as e:
                            print(f"Erreur lors du chargement du fichier {filename}: {e}")
                            continue
        return tournois
    
    def charger_joueurs(self):
        joueurs = []
        if os.path.exists("data/joueurs.json"):
            with open("data/joueurs.json", "r") as f:
                try:
                    joueurs_data = json.load(f)
                    for joueur_data in joueurs_data:
                        joueur = Joueur(
                            joueur_data["nom"],
                            joueur_data["prenom"],
                            joueur_data["date_naissance"]
                        )
                        joueurs.append(joueur)
                except json.JSONDecodeError:
                    pass
        return joueurs
    
    def demarrer(self):
        self.interface.menu_principal()
        
    def nouveau_tournoi(self, nom, lieu, date_debut, date_fin, nb_tours, description):
        self.tournoi = Tournoi(nom, lieu, date_debut, date_fin, nb_tours, [], description)
        self.tournois.append(self.tournoi)
        self.tournoi_controller = Tournoi_Controller(self.tournoi)
        self.tournoi.sauvegarder()
        return self.tournoi
    
    def nouveau_joueur(self, nom, prenom, date_naissance):
        joueur = Joueur(nom, prenom, date_naissance)
        self.joueurs.append(joueur)
        if self.tournoi:
            self.tournoi.liste_joueurs.append(joueur)
            self.tournoi.sauvegarder()
        joueur.sauvegarder()
        return joueur
        
    
    def sauvegarder_tournoi(self):
        self.tournoi.sauvegarder()
        
    def sauvegarder_joueur(self):
        for joueur in self.joueurs:
            joueur.sauvegarder()
            
    def charger_tournoi(self, nom):
        with open(f"data/tournaments/{nom}.json", "r") as f:
            data = json.load(f)
            return Tournoi(**data)
        
    def charger_joueur(self, nom):
        with open(f"data/joueurs.json", "r") as f:
            data = json.load(f)
            return Joueur(**data)  

    def get_tournois(self):
        """Récupère la liste des tournois depuis le modèle"""
        return self.tournois
    
    def get_joueurs(self):
        """Récupère la liste des joueurs depuis le modèle"""
        return self.joueurs

    def selectionner_tournoi(self, tournoi):
        """Sélectionne un tournoi et initialise son controller"""
        self.tournoi = tournoi
        self.tournoi_controller = Tournoi_Controller(self.tournoi)
        
        if tournoi.liste_joueurs:
            for joueur in tournoi.liste_joueurs:
                if joueur not in self.joueurs:
                    self.joueurs.append(joueur)


