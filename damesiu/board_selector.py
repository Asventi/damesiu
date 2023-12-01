from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.controllers.board_controller import BoardController
    from damesiu.objects import Cell

from damesiu.graphic_engine import BoardEngine
from damesiu.game_state import GameState
import curses
from threading import Lock
from damesiu.constants import directions
from damesiu.utils import EventHandler


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


class BoardSelector(EventHandler, metaclass=BoardSelectorSingleton):

    def __init__(self, board_controller: BoardController):
        self._graphic_engine = BoardEngine()
        self._board_controller = board_controller
        self._game_state = GameState()

        self._current_cell: Cell = self._board_controller.board[0][0]
        self._selected_cell: Cell | None = None
        self._playable_cells: list[Cell] = []
        self._highlight(self._current_cell)

        self._graphic_engine.on("key_pressed", self._move_cursor)

    def _move_cursor(self, key):
        self._highlight(self._current_cell)
        if key == curses.KEY_UP and self._current_cell.neighbors[directions.N]:
            self._highlight(self._current_cell.neighbors[directions.N])

        elif key == curses.KEY_DOWN and self._current_cell.neighbors[directions.S]:
            self._highlight(self._current_cell.neighbors[directions.S])

        elif key == curses.KEY_LEFT and self._current_cell.neighbors[directions.W]:
            self._highlight(self._current_cell.neighbors[directions.W])

        elif key == curses.KEY_RIGHT and self._current_cell.neighbors[directions.E]:
            self._highlight(self._current_cell.neighbors[directions.E])

        elif key == 10:
            self._select()

    def _highlight(self, cell):
        self._current_cell.highlighted = False
        cell.highlighted = True
        self._current_cell = cell

        self.update()

    def _select(self):
        if self._current_cell.pion is not None and self._current_cell.pion.player != self._game_state.current_player:
            self._graphic_engine.add_alert("Ce n'est pas votre pion ou ce n'est pas votre tour !")
            return

        if self._current_cell.playable:
            self.trigger("move_selected", source=self._selected_cell, target=self._current_cell)
            return

        if self._game_state.pion_lock is not None:
            self._graphic_engine.add_alert("Vous avez des pions a finir de manger.")
            return

        for cell in self._playable_cells:
            cell.playable = False
        self._playable_cells = []
        if self._current_cell == self._selected_cell:
            self._selected_cell.selected = False
            self._selected_cell = None
            self._current_cell.highlighted = True
        else:

            # On deselectionne l'ancienne cell selectionne et on enleve l'highlight
            if self._selected_cell is not None:
                self._selected_cell.selected = False
            self._current_cell.highlighted = False

            # On selectionne la cell et on la stock
            self._selected_cell = self._current_cell
            self._selected_cell.selected = True
            if self._selected_cell.pion is not None:
                self._playable_cells = self._selected_cell.pion.get_playable_cells()
                for cell in self._playable_cells:
                    cell.playable = True

        # On met a jour le board
        self.update()

    def update(self):
        self._graphic_engine.draw_board(self._board_controller)

    @property
    def current_cell(self):
        return self._current_cell

    @current_cell.setter
    def current_cell(self, cell: Cell):
        self._current_cell = cell
        self._highlight(cell)

    @property
    def selected_cell(self):
        return self._selected_cell

    @selected_cell.setter
    def selected_cell(self, cell: Cell):
        self._selected_cell = cell

    @property
    def playable_cells(self):
        return self._playable_cells

    @playable_cells.setter
    def playable_cells(self, cells: list[Cell]):
        self._playable_cells = cells
