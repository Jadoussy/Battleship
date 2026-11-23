# Bataille Navale (Python)
Jeu de **Bataille Navale** en ligne de commande codé en Python (version 1.0 du `14/11/26`), conçu pour deux joueurs en local avec effacement de l'écran entre les tours pour limiter l'observation de la grille adverse.

* **Python** (version : 3.12.11 64-bit)
* **Environnement de dév/test :** Spyder (version : 6.1.8 standalone)

## Fonctionnalités
* **Grilles 10×10** initialisées avec `.` (`create_grid` / `create_grid_short`) et affichées avec numérotation des lignes (`1`–`10`) et colonnes (`1`–`10`) via `display_grid`.
* **Placement de flotte** (`place_fleet`, `place_ship`, `is_valid_placement`) pour 5 navires :
  * Porte-avions (`5`)
  * Croiseur (`4`)
  * Contre-torpilleur (`3`)
  * Sous-marin (`3`)
  * Torpilleur (`2`)
* **Raccourci d'affichage en cours de placement :** saisir `my`, `hint` ou `show grid` lors de la saisie des coordonnées permet d'afficher sa grille actuelle.
* **Gestion des tirs** (`is_valid_shot`, `shoot`), détection d'un navire touché (`X`), raté (`O`), signalement d'un navire coulé (`is_ship_sunk`) et détection de la victoire (`is_fleet_destroyed`).
* **Boucle de jeu complète** (`play_game`) avec confirmation de la flotte et nettoyage du terminal (`\033[H\033[J`).

## Prérequis et lancement
* **Python 3** (utilise uniquement le module standard `time`).

Depuis un terminal dans le dossier du projet :

```bash
python main.py
