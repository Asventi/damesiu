from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.board_controller import BoardController
    from damesiu.objects import Cell

from threading import Thread
from damesiu.graphic_engine import Engine as GraphicEngine
import curses
from time import sleep
from threading import Lock


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

        self.current_cell: Cell = self.board_controller.board[0][0]
        self.selected_cell: Cell | None = None
        self.playable_cells: list[Cell] = []

        main = Thread(target=self._run)
        main.start()

    def _run(self):
        self._highlight(self.current_cell)
        while self.graphic_engine.key != 113:
            if self.graphic_engine.key == curses.KEY_UP and self.current_cell.y - 1 >= 0:
                self._highlight(self.board_controller.board[self.current_cell.y - 1][self.current_cell.x])
                # On evite la duplication de touches
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_LEFT and self.current_cell.x - 1 >= 0:
                self._highlight(self.board_controller.board[self.current_cell.y][self.current_cell.x - 1])
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_DOWN and self.current_cell.y + 1 < self.board_controller.size:
                self._highlight(self.board_controller.board[self.current_cell.y + 1][self.current_cell.x])
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_RIGHT and self.current_cell.x + 1 < self.board_controller.size:
                self._highlight(self.board_controller.board[self.current_cell.y][self.current_cell.x + 1])
                sleep(0.1)

            elif self.graphic_engine.key == 10:
                self._select()
                sleep(0.1)

    def _highlight(self, cell):
        self.current_cell.highlighted = False
        cell.highlighted = True
        self.current_cell = cell

        self.update()

    def _select(self):
        if self.current_cell.playable:
            self.trigger("move_selected", source=self.selected_cell, target=self.current_cell)
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
