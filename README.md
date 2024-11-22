# Gestionnaire de Tournois d'Échecs

Un programme en Python pour gérer des tournois d'échecs.

## Description

Ce programme permet de :
- Créer et gérer des tournois d'échecs
- Gérer une base de joueurs
- Générer automatiquement les paires de joueurs pour chaque round
- Enregistrer les résultats des matchs
- Générer différents rapports (classements, historique des matchs, etc.)

## Installation

1. Clonez le dépôt :

   `git clone [url_du_depot]`

2. Créez un environnement virtuel Python :

   `python -m venv env`

3. Activez l'environnement virtuel :

   Windows
     `env\Scripts\activate`
   Linux/Mac
     `source env/bin/activate`

4. Installez les dépendances :

   pip install -r requirements.txt

## Utilisation

1. Lancez le programme :

   `python main.py`

2. Menu Principal :
   - Nouveau tournoi : Créer un nouveau tournoi
   - Charger tournoi : Reprendre un tournoi existant
   - Rapports : Consulter les différentes statistiques
   - Quitter : Fermer le programme

### Créer un nouveau tournoi

1. Sélectionnez "Nouveau tournoi"
2. Entrez les informations du tournoi :
   - Nom
   - Lieu
   - Dates
   - Nombre de tours
   - Description
3. Ajoutez les joueurs :
   - Créez de nouveaux joueurs
4. Lancez le tournoi

### Gestion des rounds

1. Les paires sont générées automatiquement
2. Entrez les résultats des matchs :
   - 1 : Victoire joueur 1
   - 2 : Victoire joueur 2
   - 0 : Match nul

### Rapports disponibles

- Liste des joueurs (ordre alphabétique)
- Liste des tournois
- Détails d'un tournoi spécifique (joueurs, rounds, matchs)

## Structure des données

Les données sont sauvegardées en JSON dans le dossier `data/` :
- `tournaments/` : Données des tournois
- `joueurs.json` : Base de données des joueurs

## Développé avec

- Python 3.12.4
- Système de fichiers JSON pour le stockage des données

## Auteur

Thomas Jeanne
