

class Joueur:
    def __init__(self, nom, prenom, date_naissance, id_national):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_national = id_national
        
        
class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, nb_tours, liste_joueurs, description):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tours = nb_tours
        self.liste_joueurs = liste_joueurs
        self.description = description
        

class Match:
    def __init__(self, joueur1, joueur2, score_joueur1, score_joueur2):
        self.joueur1 = joueur1
        self.score_joueur1 = score_joueur1
        self.joueur2 = joueur2
        self.score_joueur2 = score_joueur2
        
class Round:
    def __init__(self, nom, date_debut, date_fin):
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        
        
