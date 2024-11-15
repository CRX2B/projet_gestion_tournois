
from modele import Tournoi, Joueur, Match, Round



class Controller:
    def __init__(self):
        self.tournoi = None
        self.joueurs = []
        self.matchs = []
        self.rounds = []
        
    def creer_tournoi(self, nom, lieu, date_debut, date_fin, nb_tours, description):
        self.tournoi = Tournoi(nom, lieu, date_debut, date_fin, nb_tours, description)
        print(f"Tournoi {nom} créé avec succès.")

        
        
