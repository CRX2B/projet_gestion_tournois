import datetime

class Round:
    def __init__(self, nom):
        self.matchs = []
        self.nom = nom
        self.date_debut = None 
        self.date_fin = None
        
    def __str__(self):
        return f"{self.nom} {self.date_debut} {self.date_fin}"
    
    def commencer_round(self):
        self.date_debut = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def terminer_round(self):
        self.date_fin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
    def to_dict(self):
        return {
            "nom": self.nom,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "matchs": [match.to_dict() for match in self.matchs]
        }

    

