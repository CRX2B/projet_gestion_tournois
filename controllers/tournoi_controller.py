import random

from models import Match, Round


class TournoiController:
    """Contrôleur gérant la logique d'un tournoi spécifique."""

    def __init__(self, tournoi):
        self.tournoi = tournoi

    def lancer_round(self):
        """Lance un nouveau round ou vérifie si un round existe deja et génère les matchs.

        Returns:
            Round: Le nouveau round créé
        """

        round_num = len(self.tournoi.rounds) + 1
        round_en_cours = None
        for round in self.tournoi.rounds:
            if round.date_fin is None:
                round_en_cours = round
                break

        if not round_en_cours:
            nouveau_round = Round(f"Round {round_num}")
            nouveau_round.commencer_round()
            # Récupère la liste des joueurs du tournoi
            joueurs = self.tournoi.liste_joueurs
            nouveau_round.matchs = self.generer_paires(joueurs)

            self.tournoi.rounds.append(nouveau_round)
            self.tournoi.sauvegarder()

            return nouveau_round
        else:
            return round_en_cours

    def cloturer_round(self, round_actuel, resultats):
        """Clôture un round en enregistrant les résultats des matchs.

        Args:
            round_actuel (Round): Round à clôturer
            resultats (list): Liste des résultats des matchs
        """

        for match, resultat in zip(
            round_actuel.matchs, resultats
        ):  # Parcourt les matchs et les résultats en parallèle
            match.resultat_match(resultat)
            match.joueur1.sauvegarder()
            match.joueur2.sauvegarder()

        round_actuel.terminer_round()
        self.tournoi.sauvegarder()

    def generer_paires(self, joueurs):
        """Génère les paires de joueurs selon le système suisse.

        Args:
            joueurs (list): Liste des joueurs
        Returns:
            list: Liste des matchs générés
        """

        round_actuel = len(self.tournoi.rounds) + 1
        matchs = []

        if round_actuel == 1:
            # Premier tour : appariement aléatoire
            random.shuffle(joueurs)
            for i in range(0, len(joueurs), 2):
                if i + 1 < len(joueurs):
                    match = Match(joueurs[i], joueurs[i + 1])
                    matchs.append(match)
        else:
            # Tours suivants : appariement selon les scores
            joueurs_tries = sorted(joueurs, key=lambda x: x.score, reverse=True)
            while joueurs_tries:
                joueur1 = joueurs_tries.pop(0)
                joueur2 = None

                # Recherche d'un adversaire qui n'a pas déjà joué contre joueur1
                for joueur in joueurs_tries:
                    if not self._ont_deja_joue(joueur1, joueur):
                        joueur2 = joueur
                        break

                if joueur2:
                    joueurs_tries.remove(joueur2)
                    match = Match(joueur1, joueur2)
                    matchs.append(match)
                else:
                    # Si aucun adversaire valide n'est trouvé, on prend le premier disponible
                    joueur2 = joueurs_tries.pop(0)
                    match = Match(joueur1, joueur2)
                    matchs.append(match)

        return matchs

    def _ont_deja_joue(self, joueur1, joueur2):
        """Vérifie si deux joueurs ont déjà joué ensemble dans ce tournoi."""
        for round in self.tournoi.rounds:
            for match in round.matchs:
                if (match.joueur1 == joueur1 and match.joueur2 == joueur2) or (
                    match.joueur1 == joueur2 and match.joueur2 == joueur1
                ):
                    return True
        return False
