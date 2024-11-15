
from modele import Tournoi, Joueur, Match, Round
from controller import Controller

class Interface:
    def __init__(self):
        self.controller = Controller()
        
    def menu_principal(self):
        print("Bienvenue dans le programme de gestion de tournoi d'échecs.")
        
    def creer_tournoi(self):
        nom = input("Entrez le nom du tournoi : ")
        lieu = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date de début du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        nb_tours = int(input("Entrez le nombre de tours du tournoi : "))
        description = input("Entrez la description du tournoi : ")
        self.controller.creer_tournoi(nom, lieu, date_debut, date_fin, nb_tours, description)
        return
    
    def ajouter_joueur(self):
        nom = input("Entrez le nom du joueur : ")
        prenom = input("Entrez le prénom du joueur : ")
        date_naissance = input("Entrez la date de naissance du joueur : ")
        id_national = input("Entrez l'ID national du joueur : ")
        self.controller.ajouter_joueur(nom, prenom, date_naissance, id_national)
        return
        
