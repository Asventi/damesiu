from damesiu.graphic_engine import Engine as GraphicEngine
from damesiu.objects import BoardController
from damesiu.objects import Player


def run():
    """
    La fonction principale du jeu
    """
    players = [Player("Joueur 1", "blanc", 0), Player("Joueur 2", "noir", 1)]
    engine = GraphicEngine()
    board = BoardController(players=players)
