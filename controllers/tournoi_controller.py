import random
import datetime

from models import Tournoi, Match, Round, Joueur

class Tournoi_Controller:
    def __init__(self, tournoi):
        self.tournoi = tournoi
        
    def lancer_round(self):
        round_num = len(self.tournoi.rounds) + 1
        nouveau_round = Round(f"Round {round_num}")
        nouveau_round.commencer_round()
        
        joueurs = self.tournoi.liste_joueurs
        nouveau_round.matchs = self.generer_paires(joueurs)
        
        self.tournoi.rounds.append(nouveau_round)
        self.tournoi.sauvegarder()
        
        return nouveau_round
                
    def cloturer_round(self, round_actuel, resultats):
        for match, resultat in zip(round_actuel.matchs, resultats):
            match.resultat_match(resultat)
            match.joueur1.sauvegarder()
            match.joueur2.sauvegarder()
            
        round_actuel.terminer_round()
        self.tournoi.sauvegarder()
    
    def generer_paires(self, joueurs):
        random.shuffle(joueurs)
        matchs = []
        for i in range(0, len(joueurs), 2):
            if i + 1 < len(joueurs):
                joueur1 = joueurs[i]
                joueur2 = joueurs[i+1]
                match = Match(joueur1, joueur2)
                matchs.append(match)
        return matchs
    


