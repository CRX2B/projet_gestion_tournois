class Rapport:
    """Gère l'affichage des rapports et statistiques."""

    def __init__(self, controller):
        self.controller = controller

    def afficher_message(self, message):
        print(message)

    def menu_rapports(self):
        """Affiche le menu des rapports."""
        self.afficher_message("\nMenu des Rapports")
        self.afficher_message("1. Liste des joueurs")
        self.afficher_message("2. Liste des tournois")
        self.afficher_message("3. Détails d'un tournoi")
        self.afficher_message("4. Retour au menu principal")

        choix = input("\nEntrez votre choix : ")

        if choix == "1":
            self.rapport_joueurs()
        elif choix == "2":
            self.rapport_tournois()
        elif choix == "3":
            self.rapport_details_tournoi()
        elif choix == "4":
            return self.controller.interface.menu_principal()
        else:
            self.afficher_message("Choix invalide")
            return self.menu_rapports()

    def rapport_joueurs(self):
        """Affiche la liste des joueurs triée par ordre alphabétique."""

        joueurs = self.controller.get_joueurs()
        if not joueurs:
            self.afficher_message("\nAucun joueur enregistré")
            return self.menu_rapports()

        self.afficher_message("\nListe des joueurs par ordre alphabétique :")
        joueurs_tries = sorted(joueurs, key=lambda x: (x.nom, x.prenom))
        for joueur in joueurs_tries:
            self.afficher_message(f"- {joueur.nom} {joueur.prenom}")

        return self.menu_rapports()

    def rapport_tournois(self):
        """Affiche la liste des tournois avec leurs informations principales."""

        tournois = self.controller.get_tournois()
        if not tournois:
            self.afficher_message("\nAucun tournoi enregistré")
            return self.menu_rapports()

        self.afficher_message("\nListe des tournois :")
        for tournoi in tournois:
            self.afficher_message(f"\nTournoi : {tournoi.nom}")
            self.afficher_message(f"Lieu : {tournoi.lieu}")
            self.afficher_message(f"Date : {tournoi.date_debut} - {tournoi.date_fin}")
            self.afficher_message(f"Nombre de joueurs : {len(tournoi.liste_joueurs)}")

        return self.menu_rapports()

    def rapport_details_tournoi(self):
        """Affiche les détails d'un tournoi spécifique."""
        tournois = self.controller.get_tournois()
        if not tournois:
            self.afficher_message("\nAucun tournoi enregistré")
            return self.menu_rapports()

        self.afficher_message("\nSélectionnez un tournoi :")
        for i, tournoi in enumerate(tournois, 1):
            self.afficher_message(f"{i}. {tournoi.nom}")

        choix = input("\nNuméro du tournoi (ou 'q' pour revenir) : ")
        if choix.lower() == "q":
            return self.menu_rapports()

        try:  # Convertit la saisie en entier et vérifie si l'index est valide
            index = int(choix) - 1
            if 0 <= index < len(tournois):
                tournoi = tournois[index]
                self.afficher_details_tournoi(tournoi)
            else:
                self.afficher_message("Numéro de tournoi invalide")
        except ValueError:  # Gère les erreurs de conversion en entier
            self.afficher_message("Entrée invalide")

        return self.menu_rapports()

    def afficher_details_tournoi(self, tournoi):
        """Affiche les détails complets d'un tournoi."""

        self.afficher_message(f"\nDétails du tournoi : {tournoi.nom}")
        self.afficher_message(f"Lieu : {tournoi.lieu}")
        self.afficher_message(f"Date : {tournoi.date_debut} - {tournoi.date_fin}")
        self.afficher_message(f"Nombre de tours : {tournoi.nb_tours}")
        self.afficher_message(f"Description : {tournoi.description}")

        if tournoi.liste_joueurs:  # Si le tournoi a des joueurs
            self.afficher_message("\nListe des joueurs :")
            joueurs_tries = sorted(tournoi.liste_joueurs, key=lambda x: (-x.score, x.nom))
            for joueur in joueurs_tries:
                self.afficher_message(f"- {joueur.nom} {joueur.prenom} (Score: {joueur.score})")

        if tournoi.rounds:  # Si le tournoi a des rounds
            self.afficher_message("\nRounds :")
            for round in tournoi.rounds:
                self.afficher_message(f"\n{round.nom}")
                self.afficher_message(f"Début : {round.date_debut}")
                self.afficher_message(f"Fin : {round.date_fin or 'En cours'}")
                for match in round.matchs:
                    self.afficher_message(f"- {match}")
