import random

from models import Match, Round


class TournoiController:
    """Contrôleur gérant la logique d'un tournoi spécifique."""

    def __init__(self, tournoi):
        self.tournoi = tournoi

    def lancer_round(self):
        """Lance un nouveau round du tournoi."""

        round_num = len(self.tournoi.rounds) + 1
        nouveau_round = Round(f"Round {round_num}")
        nouveau_round.commencer_round()
        # Récupère la liste des joueurs du tournoi
        joueurs = self.tournoi.liste_joueurs
        nouveau_round.matchs = self.generer_paires(joueurs)

        self.tournoi.rounds.append(nouveau_round)
        self.tournoi.sauvegarder()

        return nouveau_round

    def cloturer_round(self, round_actuel, resultats):
        """Clôture un round en enregistrant les résultats."""

        for match, resultat in zip(
            round_actuel.matchs, resultats
        ):  # Parcourt les matchs et les résultats en parallèle
            match.resultat_match(resultat)
            match.joueur1.sauvegarder()
            match.joueur2.sauvegarder()

        round_actuel.terminer_round()
        self.tournoi.sauvegarder()

    def generer_paires(self, joueurs):
        """Génère les paires de joueurs pour les matchs."""

        # Mélange aléatoire des joueurs pour créer des paires aléatoires
        random.shuffle(joueurs)
        matchs = []
        # Parcourt la liste par pas de 2 pour créer les paires
        for i in range(0, len(joueurs), 2):
            if i + 1 < len(joueurs):
                joueur1 = joueurs[i]
                joueur2 = joueurs[i + 1]
                match = Match(joueur1, joueur2)
                matchs.append(match)
        return matchs
