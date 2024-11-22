class Match:
    def __init__(self, joueur1, joueur2, score_joueur1=0, score_joueur2=0):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score_joueur1 = score_joueur1
        self.score_joueur2 = score_joueur2
        
    def __str__(self):
        return f"{self.joueur1.nom} {self.joueur1.prenom} ({self.score_joueur1}) vs {self.joueur2.nom} {self.joueur2.prenom} ({self.score_joueur2})"
    
    def resultat_match(self, resultat):
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
        return {
            "joueur1": self.joueur1.to_dict(),
            "joueur2": self.joueur2.to_dict(),
            "score_joueur1": self.score_joueur1,
            "score_joueur2": self.score_joueur2
        }

    @property
    def joueurs(self):
        return [self.joueur1, self.joueur2]



