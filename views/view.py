from .rapport import Rapport


class Interface:
    """Classe gérant l'interface utilisateur et l'affichage."""

    def __init__(self, controller):
        """Initialise l'interface avec le contrôleur.

        Args:
            controller: Instance du contrôleur principal
        """
        self.controller = controller
        self.rapport = Rapport(controller)

    def afficher_message(self, message):
        """Affiche un message à l'utilisateur.

        Args:
            message (str): Message à afficher
        """
        print(message)

    def menu_principal(self):
        """Affiche et gère le menu principal.

        Returns:
            function: Retourne la méthode du menu sélectionné
        """
        self.afficher_message("\nGestion de tournois d'échecs")
        self.afficher_message("1. Créer un nouveau tournoi")
        self.afficher_message("2. Charger un tournoi existant")
        self.afficher_message("3. Voir les rapports")
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
        """Affiche et gère le menu de création d'un nouveau tournoi.

        Returns:
            function: Retourne la méthode correspondant au choix de l'utilisateur
        """
        self.afficher_message("\nCréation d'un nouveau tournoi")
        self.afficher_message("1. Créer le tournoi")
        self.afficher_message("2. Ajouter des joueurs")
        self.afficher_message("3. Commencer le tournoi")
        self.afficher_message("4. Retour au menu principal")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            self.prompt_creer_tournoi()
        elif choix == "2":
            if self.controller.tournoi is None:
                self.afficher_message("Veuillez créer un tournoi avant d'ajouter un joueur.")
                return self.menu_nouveau_tournoi()
            self.prompt_nouveau_joueur()
        elif choix == "3":
            if self.controller.tournoi is None:
                self.afficher_message("Veuillez créer un tournoi avant de commencer.")
                return self.menu_nouveau_tournoi()
            if len(self.controller.tournoi.liste_joueurs) < 2:
                self.afficher_message("Il faut au moins 2 joueurs pour commencer un tournoi.")
                return self.menu_nouveau_tournoi()
            self.gestion_round()
        elif choix == "4":
            return self.menu_principal()
        else:
            print("Choix invalide. Veuillez réessayer.")
            return self.menu_nouveau_tournoi()

    def menu_charger_tournoi(self):
        """Affiche et gère le menu de chargement d'un tournoi existant.

        Returns:
            function: Retourne au menu principal ou gère le tournoi sélectionné
        """
        tournois = self.controller.get_tournois()
        if not tournois:
            self.afficher_message("\nAucun tournoi enregistré.")
            return self.menu_principal()

        self.afficher_message("\nTournois disponibles :")
        for i, tournoi in enumerate(tournois, 1):
            self.afficher_message(f"{i}. {tournoi.nom} ({tournoi.lieu})")
        self.afficher_message(f"{len(tournois) + 1}. Retour au menu principal")

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
        self.afficher_message("\nGestion du tournoi")
        self.afficher_message(f"Tournoi : {self.controller.tournoi.nom}")
        self.afficher_message("1. Voir les détails")
        self.afficher_message("2. Ajouter des joueurs")
        self.afficher_message("3. Commencer/Continuer le tournoi")
        self.afficher_message("4. Retour au menu principal")

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
        """Gère la création d'un nouveau tournoi via les entrées utilisateur.

        Returns:
            function: Retourne au menu nouveau tournoi
        """
        nom = input("Entrez le nom du tournoi : ")
        lieu = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date de début du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        nb_tours = int(input("Entrez le nombre de tours du tournoi : "))
        description = input("Entrez la description du tournoi : ")
        self.controller.nouveau_tournoi(nom, lieu, date_debut, date_fin, nb_tours, description)
        self.afficher_message("Tournoi créé avec succès!")
        return self.menu_principal()

    def prompt_nouveau_joueur(self):
        """Gère l'ajout d'un nouveau joueur via les entrées utilisateur.

        Returns:
            function: Retourne au menu nouveau tournoi ou continue l'ajout de joueurs
        """
        if self.controller.tournoi is None:
            self.afficher_message("Veuillez créer un tournoi avant d'ajouter un joueur.")
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
        self.afficher_message("Joueur ajouté avec succès!")
        return self.prompt_nouveau_joueur()

    def gestion_round(self):
        """Gère le déroulement d'un round : affichage des matchs et saisie des résultats.

        Returns:
            function: Retourne au menu principal une fois le round terminé
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
            self.afficher_message(
                f"{match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}"
            )

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

    def afficher_matchs(self, matchs):
        """Affiche la liste des matchs d'un round.

        Args:
            matchs (Round): Instance du round contenant les matchs à afficher
        """
        self.afficher_message(f"Matchs du round {matchs.nom} :")
        for match in matchs.matchs:
            self.afficher_message(
                f"{match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}"
            )

    def prompt_resultat_match(self, match):
        """Demande et valide le résultat d'un match.

        Args:
            match (Match): Instance du match dont on veut le résultat

        Returns:
            str: '1' pour victoire joueur1, '2' pour victoire joueur2, '0' pour match nul
        """
        self.afficher_message(
            f"Match : {match.joueur1.nom} {match.joueur1.prenom} vs {match.joueur2.nom} {match.joueur2.prenom}"
        )
        resultat = input("Résultat (1=joueur1 gagne, 2=joueur2 gagne, 0=match nul) : ")
        return resultat

    def afficher_liste_joueurs(self):
        """Affiche la liste de tous les joueurs enregistrés.

        Returns:
            function: Retourne au menu des rapports
        """
        joueurs = self.controller.get_joueurs()
        if not joueurs:
            self.afficher_message("Aucun joueur enregistré.")
        else:
            self.afficher_message("\nListe des joueurs :")
            for joueur in joueurs:
                self.afficher_message(f"Nom: {joueur.nom}")
                self.afficher_message(f"Prenom: {joueur.prenom}")
                self.afficher_message(f"ID National: {joueur.id_national}")
            self.afficher_message("")
        return self.menu_principal()

    def afficher_liste_tournois(self):
        """Affiche la liste de tous les tournois enregistrés.

        Returns:
            function: Retourne au menu des rapports
        """
        tournois = self.controller.get_tournois()
        if not tournois:
            self.afficher_message("Aucun tournoi enregistré.")
        else:
            self.afficher_message("\nListe des tournois :")
            for tournoi in tournois:
                self.afficher_message(f"\nNom: {tournoi.nom}")
                self.afficher_message(f"Lieu: {tournoi.lieu}")
                self.afficher_message(f"Date de début: {tournoi.date_debut}")
                self.afficher_message(f"Date de fin: {tournoi.date_fin}")
                self.afficher_message(f"Nombre de tours: {tournoi.nb_tours}")
                self.afficher_message(f"Description: {tournoi.description}")
                if tournoi.liste_joueurs:
                    self.afficher_message("\nListe des joueurs :")
                    for joueur in tournoi.liste_joueurs:
                        self.afficher_message(f"Nom: {joueur.nom}")
                        self.afficher_message(f"Prenom: {joueur.prenom}")
                        self.afficher_message(f"ID National: {joueur.id_national}")
                self.afficher_message("")
        return self.menu_principal()

    def afficher_classement(self):
        """Affiche le classement actuel des joueurs du tournoi en cours.

        Note:
            Les joueurs sont triés par score décroissant puis par nom
        """
        self.afficher_message("\nClassement final :")
        joueurs_tries = sorted(self.controller.tournoi.liste_joueurs, key=lambda x: (-x.score, x.nom))
        for i, joueur in enumerate(joueurs_tries, 1):
            self.afficher_message(f"{i}. {joueur.nom} {joueur.prenom} - Score: {joueur.score}")
