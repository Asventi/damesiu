from damesiu.objects import BoardController
from damesiu.objects import Player
from damesiu.board_selector import BoardSelector
from damesiu.graphic_engine import Engine


def run():
    """
    La fonction principale du jeu
    """
    players = [Player("Joueur 1", "blanc", 0), Player("Joueur 2", "noir", 1)]
    board = BoardController(players=players)
    board_selector = BoardSelector(board)
    graphic_engine = Engine()
    graphic_engine.add_message('test de message')


