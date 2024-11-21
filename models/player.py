import json
import os

class Joueur:
    def __init__(self, nom, prenom, date_naissance, id_national):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_national = id_national
        
    def __str__(self):
        return f"{self.nom} {self.prenom} {self.id_national}"
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "id_national": self.id_national
        }

    def sauvegarder(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            
        fichier = "data/joueurs.json"
        donnees = self.to_dict()
        
        # Charger les joueurs existants
        joueurs_existants = []
        if os.path.exists(fichier):
            with open(fichier, "r") as f:
                try:
                    joueurs_existants = json.load(f)
                    if not isinstance(joueurs_existants, list):
                        joueurs_existants = [joueurs_existants]
                except json.JSONDecodeError:
                    joueurs_existants = []
        
        # Ajouter le nouveau joueur
        joueurs_existants.append(donnees)
        
        # Sauvegarder tous les joueurs
        with open(fichier, "w") as f:
            json.dump(joueurs_existants, f, indent=4)
