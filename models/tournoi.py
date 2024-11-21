import json
from datetime import datetime
import os

class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, nb_tours, liste_joueurs, description):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tours = nb_tours
        self.liste_joueurs = liste_joueurs
        self.description = description
        
    def __str__(self):
        return f"{self.nom} {self.lieu} {self.date_debut} {self.date_fin} {self.nb_tours} {self.liste_joueurs} {self.description}"
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nb_tours": self.nb_tours,
            "liste_joueurs": [joueur.to_dict() for joueur in self.liste_joueurs],
            "description": self.description 
        }
    
    def sauvegarder(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")
            
        fichier = f"data/tournaments/{self.nom}.json"
        donnees = self.to_dict()
        
        with open(fichier, "w") as f:
            json.dump(donnees, f, indent=4)
                    
