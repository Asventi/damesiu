from damesiu.board_controller import BoardController
from damesiu.objects import Player
from damesiu.board_selector import BoardSelector
from damesiu.graphic_engine import Engine
from damesiu.objects import Cell
from time import sleep
from threading import Thread


class GameController:
    def __init__(self):
        playername = "Asventi"  # input('Entre ton nom de joueur  : \n ')
        self.size = 10  # int(input('Quel taille de tableau : () \n'))
        self.players = [Player("Joueur 1", "blanc", 0), Player(playername, "noir", 1)]
        self.board_controller = BoardController(players=self.players, size=self.size)
        self.board_selector = BoardSelector(self.board_controller)
        self.graphic_engine = Engine()
        self.graphic_engine.add_message(f'La partie commence {self.players[1].name}')
        self.board_selector.on("move_selected", self.move)
        main = Thread(target=self.run)
        main.start()

    def run(self):
        """
        La fonction principale du jeu
        """
        # while self.graphic_engine.key != 113:
        #     if self.graphic_engine.key == 114:
        #         self.board_controller.starter()
        pass

    def move(self, source: Cell, target: Cell):
        self.graphic_engine.add_message(f'{source} -> {target}')
        target.pion = source.pion
        source.pion = None
        self.graphic_engine.draw_board(self.board_controller)
