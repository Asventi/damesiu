from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.controllers.board_controller import BoardController
    from damesiu.objects import Cell

from damesiu.graphic_engine import Engine as GraphicEngine
from damesiu.game_state import GameState
import curses
from threading import Lock
from damesiu.constants import directions

class BoardSelectorSingleton(type):
    """
    Thread safe singleton for Board Selector
    """
    _instances = {}
    # Pour lock les thread pour eviter que deux thread instancie la classe en meme temps ce qui casserai le singleton
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Fonction de creation d'instance
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class EventHandler(object):
    callbacks = None

    def on(self, eh_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if eh_name not in self.callbacks:
            self.callbacks[eh_name] = [callback]
        else:
            self.callbacks[eh_name].append(callback)

    def trigger(self, eh_name, **kwargs):
        if self.callbacks is not None and eh_name in self.callbacks:
            for callback in self.callbacks[eh_name]:
                callback(**kwargs)


class BoardSelector(EventHandler, metaclass=BoardSelectorSingleton):

    def __init__(self, board_controller: BoardController):
        self.graphic_engine = GraphicEngine()
        self.board_controller = board_controller
        self.game_state = GameState()

        self.current_cell: Cell = self.board_controller.board[0][0]
        self.selected_cell: Cell | None = None
        self.playable_cells: list[Cell] = []
        self._highlight(self.current_cell)

        self.graphic_engine.on("key_pressed", self._move_cursor)

    def _move_cursor(self, key):
        self._highlight(self.current_cell)
        if key == curses.KEY_UP and self.current_cell.neighbors[directions.N]:
            self._highlight(self.current_cell.neighbors[directions.N])

        elif key == curses.KEY_DOWN and self.current_cell.neighbors[directions.S]:
            self._highlight(self.current_cell.neighbors[directions.S])

        elif key == curses.KEY_LEFT and self.current_cell.neighbors[directions.W]:
            self._highlight(self.current_cell.neighbors[directions.W])

        elif key == curses.KEY_RIGHT and self.current_cell.neighbors[directions.E]:
            self._highlight(self.current_cell.neighbors[directions.E])

        elif key == 10:
            self._select()

    def _highlight(self, cell):
        self.current_cell.highlighted = False
        cell.highlighted = True
        self.current_cell = cell

        self.update()

    def _select(self):
        if self.current_cell.pion is not None and self.current_cell.pion.player != self.game_state.current_player:
            self.graphic_engine.add_alert("Ce n'est pas votre pion ou ce n'est pas votre tour !")
            return

        if self.current_cell.playable:
            self.trigger("move_selected", source=self.selected_cell, target=self.current_cell)
            return

        if self.game_state.pion_lock is not None:
            self.graphic_engine.add_alert("Vous avez des pions a finir de manger.")
            return

        for cell in self.playable_cells:
            cell.playable = False
        self.playable_cells = []
        if self.current_cell == self.selected_cell:
            self.selected_cell.selected = False
            self.selected_cell = None
            self.current_cell.highlighted = True
        else:

            # On deselectionne l'ancienne cell selectionne et on enleve l'highlight
            if self.selected_cell is not None:
                self.selected_cell.selected = False
            self.current_cell.highlighted = False

            # On selectionne la cell et on la stock
            self.selected_cell = self.current_cell
            self.selected_cell.selected = True
            if self.selected_cell.pion is not None:
                self.playable_cells = self.selected_cell.pion.get_playable_cells()
                for cell in self.playable_cells:
                    cell.playable = True

        # On met a jour le board
        self.update()

    def update(self):
        self.graphic_engine.draw_board(self.board_controller)
