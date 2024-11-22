from .rapport import Rapport


class Interface:
    """Interface utilisateur principale de l'application."""

    def __init__(self, controller):
        self.controller = controller
        self.rapport = Rapport(controller)

    def afficher_message(self, message):
        print(message)

    def menu_principal(self):
        """Affiche et gère le menu principal de l'application."""
        self.afficher_message("\nMenu Principal")
        self.afficher_message("1. Nouveau tournoi")
        self.afficher_message("2. Charger tournoi")
        self.afficher_message("3. Rapports")
        self.afficher_message("4. Quitter")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            self.menu_nouveau_tournoi()
        elif choix == "2":
            self.menu_charger_tournoi()
        elif choix == "3":
            retour = self.rapport.menu_rapports()
            if retour == "menu_principal":
                return self.menu_principal()
        elif choix == "4":
            self.afficher_message("Au revoir !")
            exit()
        else:
            self.afficher_message("Choix invalide. Veuillez réessayer.")
            return self.menu_principal()

    def menu_nouveau_tournoi(self):
        """Affiche et gère le menu de création d'un nouveau tournoi."""
        self.afficher_message("\nNouveau Tournoi")
        self.afficher_message("1. Créer un tournoi")
        self.afficher_message("2. Ajouter des joueurs")
        self.afficher_message("3. Commencer le tournoi")
        self.afficher_message("4. Retour au menu principal")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            self.prompt_creer_tournoi()
        elif choix == "2":
            if self.controller.tournoi is None:
                print("Veuillez créer un tournoi avant d'ajouter un joueur.")
                return self.menu_nouveau_tournoi()
            self.prompt_nouveau_joueur()
        elif choix == "3":
            if self.controller.tournoi is None:
                print("Veuillez créer un tournoi avant de commencer.")
                return self.menu_nouveau_tournoi()
            if len(self.controller.tournoi.liste_joueurs) < 2:
                print("Il faut au moins 2 joueurs pour commencer un tournoi.")
                return self.menu_nouveau_tournoi()
            self.gestion_round()
        elif choix == "4":
            return self.menu_principal()
        else:
            print("Choix invalide. Veuillez réessayer.")
            return self.menu_nouveau_tournoi()

    def menu_charger_tournoi(self):
        """Affiche et gère le menu de chargement d'un tournoi."""
        tournois = self.controller.get_tournois()
        if not tournois:
            print("\nAucun tournoi enregistré.")
            return self.menu_principal()

        print("\nTournois disponibles :")
        for i, tournoi in enumerate(tournois, 1):
            print(f"{i}. {tournoi.nom} ({tournoi.lieu})")
        print(f"{len(tournois) + 1}. Retour au menu principal")

        choix = input("\nSélectionnez un tournoi : ")
        try:
            choix_num = int(choix)
            if choix_num == len(tournois) + 1:
                return self.menu_principal()
            if 1 <= choix_num <= len(tournois):
                self.controller.selectionner_tournoi(tournois[choix_num - 1])
                return self.menu_gestion_tournoi()
        except ValueError:
            pass

        print("Choix invalide. Veuillez réessayer.")
        return self.menu_charger_tournoi()

    def menu_gestion_tournoi(self):
        """Menu de gestion d'un tournoi chargé"""
        print("\nGestion du tournoi")
        print(f"Tournoi : {self.controller.tournoi.nom}")
        print("1. Voir les détails")
        print("2. Ajouter des joueurs")
        print("3. Commencer/Continuer le tournoi")
        print("4. Retour au menu principal")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            self.rapport.afficher_details_tournoi(self.controller.tournoi)
            return self.menu_gestion_tournoi()
        elif choix == "2":
            self.prompt_nouveau_joueur()
            return self.menu_gestion_tournoi()
        elif choix == "3":
            if len(self.controller.tournoi.liste_joueurs) < 2:
                print("Il faut au moins 2 joueurs pour commencer un tournoi.")
                return self.menu_gestion_tournoi()
            self.gestion_round()
        elif choix == "4":
            return self.menu_principal()
        else:
            print("Choix invalide. Veuillez réessayer.")
            return self.menu_gestion_tournoi()

    def afficher_details_tournoi(self):
        """Affiche les détails du tournoi sélectionné."""
        tournoi = self.controller.tournoi
        print(f"\nDétails du tournoi : {tournoi.nom}")
        print(f"Lieu : {tournoi.lieu}")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre de tours : {tournoi.nb_tours}")
        print(f"Description : {tournoi.description}")

        if tournoi.liste_joueurs:
            print("\nListe des joueurs :")
            for joueur in tournoi.liste_joueurs:
                print(f"- {joueur.nom} {joueur.prenom} (ID: {joueur.id_national})")

    def prompt_creer_tournoi(self):
        """Prompt pour créer un nouveau tournoi."""
        nom = input("Entrez le nom du tournoi : ")
        lieu = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date de début du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        nb_tours = int(input("Entrez le nombre de tours du tournoi : "))
        description = input("Entrez la description du tournoi : ")
        self.controller.nouveau_tournoi(nom, lieu, date_debut, date_fin, nb_tours, description)
        print("Tournoi créé avec succès!")
        return self.menu_principal()

    def prompt_nouveau_joueur(self):
        """Prompt pour ajouter un nouveau joueur."""
        if self.controller.tournoi is None:
            print("Veuillez créer un tournoi avant d'ajouter un joueur.")
            return self.menu_principal()

        nom = input("Entrez le nom du joueur ou 'q' pour quitter: ")
        if nom == "q":
            return self.menu_principal()
        prenom = input("Entrez le prénom du joueur ou 'q' pour quitter: ")
        if prenom == "q":
            return self.menu_principal()
        date_naissance = input("Entrez la date de naissance du joueur (format JJ/MM/AAAA) ou 'q' pour quitter: ")
        if date_naissance == "q":
            return self.menu_principal()
        self.controller.nouveau_joueur(nom, prenom, date_naissance)
        print("Joueur ajouté avec succès!")
        return self.prompt_nouveau_joueur()

    def charger_tournoi(self):
        """Affiche la liste des tournois enregistrés"""
        tournois = self.controller.get_tournois()
        if not tournois:
            print("Aucun tournoi enregistré.")
        else:
            print("\nListe des tournois :")
            for tournoi in tournois:
                print(f"\nNom: {tournoi.nom}")
                print(f"Lieu: {tournoi.lieu}")
                print(f"Date de début: {tournoi.date_debut}")
                print(f"Date de fin: {tournoi.date_fin}")
                print(f"Nombre de tours: {tournoi.nb_tours}")
                print(f"Description: {tournoi.description}")
                if tournoi.liste_joueurs:
                    print("\nListe des joueurs :")
                    for joueur in tournoi.liste_joueurs:
                        print(f"Nom: {joueur.nom}")
                        print(f"Prenom: {joueur.prenom}")
                        print(f"ID National: {joueur.id_national}")
                print()
        return self.menu_principal()

    def charger_joueur(self):
        """Affiche la liste des joueurs enregistrés"""
        joueurs = self.controller.get_joueurs()
        if not joueurs:
            print("Aucun joueur enregistré.")
        else:
            print("\nListe des joueurs :")
            for joueur in joueurs:
                print(f"Nom: {joueur.nom}")
                print(f"Prenom: {joueur.prenom}")
                print(f"ID National: {joueur.id_national}")
            print()
        return self.menu_principal()

    def afficher_matchs(self, matchs):
        """Affiche les matchs d'un round."""
        print(f"Matchs du round {matchs.nom} :")
        for match in matchs.matchs:
            print(f"{match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}")

    def prompt_resultat_match(self, match):
        """Prompt pour entrer le résultat d'un match."""
        print(f"Match : {match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}")
        resultat = input("Résultat (1=joueur1 gagne, 2=joueur2 gagne, 0=match nul) : ")
        return resultat

    def gestion_round(self):
        """Gère le déroulement d'un round du tournoi.

        Affiche les matchs, collecte les résultats et met à jour les scores.
        """
        if not self.controller.tournoi_controller:
            print("Erreur: Pas de tournoi sélectionné")
            return self.menu_principal()

        round_actuel = self.controller.tournoi_controller.lancer_round()
        # Affiche le nom du round en cours
        print(f"\nRound {round_actuel.nom}")
        # Affiche les matchs générés pour le round en cours
        print("Matchs générés :")
        for match in round_actuel.matchs:
            print(f"- {match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}")

        resultats = []
        print("\nEntrez les résultats des matchs :")
        for match in round_actuel.matchs:
            resultat = self.prompt_resultat_match(match)
            resultats.append(resultat)

        self.controller.tournoi_controller.cloturer_round(round_actuel, resultats)
        # Vérifie si le tournoi est terminé
        if len(self.controller.tournoi.rounds) >= self.controller.tournoi.nb_tours:
            print("\nTournoi terminé !")
            self.afficher_classement()
            return self.menu_principal()
        # Si le tournoi n'est pas terminé, propose de passer au round suivant
        else:
            print("\nRound terminé. Passez au round suivant ?")
            choix = input("1. Oui\n2. Non\nVotre choix : ")
            if choix == "1":
                return self.gestion_round()
            else:
                return self.menu_principal()

    def afficher_classement(self):
        """Affiche le classement final du tournoi"""
        print("\nClassement final :")
        # Trie les joueurs par score décroissant, puis par nom en cas d'égalité
        joueurs_tries = sorted(self.controller.tournoi.liste_joueurs, key=lambda x: (-x.score, x.nom))
        for i, joueur in enumerate(joueurs_tries, 1):
            print(f"{i}. {joueur.nom} {joueur.prenom} - Score: {joueur.score}")
