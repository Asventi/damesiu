import os
from typing import Dict, List


def game_parameters() -> List[Dict]:
    """
    Renvoie les parametres des joueurs et si ils sont des IA ou non
    sous forme de liste de dictionnaire

    :return: Liste des parametres des joueurs
    :rtype: List[Dict]
    """
    cls()
    print("Configuration joueur 1 : \n\n")
    player1_is_ia = input("Joueur 1 est une IA ? (y/n) : ")
    if player1_is_ia == "y":
        player1_is_ia = True
        cls()
        player1_name = "IA_1"
    else:
        player1_is_ia = False
        cls()
        print("Configuration joueur 1 : \n\n")
        player1_name = input("Nom du joueur 1 : ")
        cls()

    print("Configuration joueur 2 : \n\n")
    player2_is_ia = input("Joueur 2 est une IA ? (y/n) : ")
    if player2_is_ia == "y":
        player2_is_ia = True
        cls()
        player2_name = "IA_2"
    else:
        player2_is_ia = False
        cls()
        print("Configuration joueur 2 : \n\n")
        player2_name = input("Nom du joueur 2 : ")
        cls()
    return [{
        "name": player1_name,
        "color": "white",
        "is_ia": player1_is_ia,
        "playercode": 0
    },
        {
            "name": player2_name,
            "color": "black",
            "is_ia": player2_is_ia,
            "playercode": 1

        }]


def cls() -> None:
    """
    Fonction pour clear le terminal, fonctionne sur windows et linux
    """
    os.system('cls' if os.name == 'nt' else 'clear')
