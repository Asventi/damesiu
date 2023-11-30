from damesiu.controllers.board_controller import BoardController
from damesiu.objects import Player
from damesiu.board_selector import BoardSelector
from damesiu.graphic_engine import Engine
from damesiu.game_state import GameState
from damesiu.objects import Cell
from threading import Thread
from time import sleep


class GameController:
    def __init__(self):
        playername = "Asventi"  # input('Entre ton nom de joueur  : \n ')
        self.size = 10  # int(input('Quel taille de tableau : () \n'))
        self.players = [Player("IA", "blanc", 0, is_ia=True), Player(playername, "noir", 1, is_ia=True)]
        self.board_controller = BoardController(players=self.players, size=self.size)
        self.board_selector = BoardSelector(self.board_controller)
        self.graphic_engine = Engine()
        self.game_state = GameState()
        self.game_state.current_player = self.players[0]

        self.graphic_engine.add_message(f'La partie commence {self.players[1].name}')
        self.board_selector.on("move_selected", self.move)
        self.graphic_engine.on("key_pressed", self.reset)
        for player in self.players:
            if player.is_ia:
                player.ia.on("move", self.move)
        self.end_turn()

    def end_turn(self):
        """
        Fin du tour
        """
        if self.players[0].score == 20 or self.players[1].score == 20:
            self.graphic_engine.add_message(f'Le joueur {self.game_state.current_player.name} a gagne')
            sleep(5)
            exit()
        if self.game_state.current_player == self.players[1]:
            self.game_state.current_player = self.players[0]
        else:
            self.game_state.current_player = self.players[1]
        self.graphic_engine.add_message(f'C\'est au tour de {self.game_state.current_player.name}')
        if self.game_state.current_player.is_ia:
            self.graphic_engine.add_message(f'{self.game_state.current_player.name} joue')
            self.game_state.current_player.ia.turn(board=self.board_controller)

    def move(self, source: Cell, target: Cell):
        eat_move = False
        for cell in self.board_selector.playable_cells:
            cell.playable = False
        self.board_selector.playable_cells = []
        self.board_selector.selected_cell.selected = False
        self.board_selector.selected_cell = None

        if abs(source.x - target.x) > 1 or abs(source.y - target.y) > 1:
            eat_move = True
            eat_x = source.x + (target.x - source.x) // 2
            eat_y = source.y + (target.y - source.y) // 2
            source.pion.player.score += 1
            self.board_controller.board[eat_y][eat_x].pion = None

        target.pion = source.pion
        source.pion = None
        if eat_move:
            playable_cells = target.pion.get_playable_cells("all")
            if len(playable_cells) > 0:
                self.game_state.pion_lock = target.pion
                if self.game_state.current_player.is_ia:
                    self.graphic_engine.draw_board(self.board_controller)
                    self.game_state.current_player.ia.turn(board=self.board_controller)
                    return
                else:
                    self.board_selector.playable_cells = playable_cells
                    for cell in self.board_selector.playable_cells:
                        cell.playable = True
                    target.selected = True
                    self.board_selector.selected_cell = target
                    self.board_selector.current_cell.highlighted = False
            else:
                self.game_state.pion_lock = None

        self.graphic_engine.draw_board(self.board_controller)
        if self.game_state.pion_lock is None:
            self.graphic_engine.clear_alert()
            self.end_turn()

    def reset(self, key):
        if key == 114:
            self.board_controller.starter()
