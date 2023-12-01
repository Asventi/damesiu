from typing import Optional

from damesiu.controllers.board_controller import BoardController
from damesiu.objects import Player
from damesiu.board_selector import BoardSelector
from damesiu.graphic_engine import GraphicEngine
from damesiu.game_state import GameState
from damesiu.objects import Cell
from time import sleep
from damesiu import ia

class GameController:
    def __init__(self):
        playername = "Asventi"  # input('Entre ton nom de joueur  : \n ')
        self.size = 10  # int(input('Quel taille de tableau : () \n'))
        self.players = [Player("IA", "blanc", 0, is_ia=True), Player(playername, "noir", 1, is_ia=False)]
        self.board_controller = BoardController(players=self.players, size=self.size)
        self.board_selector = BoardSelector(self.board_controller)
        self.graphic_engine = GraphicEngine()
        self.game_state = GameState()
        self.game_state.current_player = self.players[0]

        self.graphic_engine.add_message(f'La partie commence {self.players[1].name}')
        self.board_selector.on("move_selected", self.move)
        self.end_turn()

    def end_turn(self):
        """
        Gere la fin du tour du tour et lance le tour du prochain, si c'est une ia lance la fonction turn de l'ia
        """
        if self.game_state.game_ended:
            return
        if self.game_state.current_player == self.players[1]:
            self.game_state.current_player = self.players[0]
        else:
            self.game_state.current_player = self.players[1]
        self.graphic_engine.add_message(f'C\'est au tour de {self.game_state.current_player.name}')
        if self.game_state.current_player.is_ia:
            self.graphic_engine.add_message(f'{self.game_state.current_player.name} joue')
            ia.turn(board=self.board_controller, game_controller=self)

    def move(self, source: Optional[Cell], target: Optional[Cell]):
        """
        Gere le deplacement d'un pion en fonction de la cellule source et la cellule cible, gere automatiquement les
        cas ou le joueur doit manger un pion adverse, si un mouvement multiple est possible, le pion bougé sera bloqué
        et seulement les mouvements sautés de ce pion seront jouable par le joueur detenteur du pion.
        Si la source et la target sont None, alors le jeu est fini. Oblige le joueur a jouer un mouvement ou il peut
        manger un pion adverse, si il y en a.

        :param source: Cellule source du pion, ne doit pas etre sans pion
        :param target: Cellule cible du pion, ne doit pas avoir de pion
        """
        if source is None and target is None:
            self.graphic_engine.add_message(f'Plus aucun mouvement possible, le jeu est fini.')
            self.game_state.game_ended = True
            sleep(5)
            exit()

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
            self.game_state.current_player.score += 1
            self.board_controller.board[eat_y][eat_x].pion.delete()
        elif not self.game_state.current_player.is_ia:
            # Verifier l'existence de saut possibles
            pass

        target.pion = source.pion
        source.pion = None
        if eat_move:
            playable_cells = target.pion.get_playable_cells("all")
            if len(playable_cells) > 0:
                self.game_state.pion_lock = target.pion
                if self.game_state.current_player.is_ia:
                    self.graphic_engine.draw_board(self.board_controller)
                    ia.turn(board=self.board_controller, game_controller=self)
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
        if (target.pion.color == "white" and target.pion.y == self.size - 1 or target.pion.color == "black"
                and target.pion.y == 0):
            self.graphic_engine.add_message(
                f'{self.game_state.current_player.name} a fait une dame et gagne 2 points de score')
            self.game_state.current_player.score += 2
            target.pion.delete()
            sleep(1)
            self.graphic_engine.draw_board(self.board_controller)

        if self.game_state.pion_lock is None:
            self.graphic_engine.clear_alert()
            self.end_turn()
