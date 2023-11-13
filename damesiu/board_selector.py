from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import BoardController

from threading import Thread
from damesiu.graphic_engine import Engine as GraphicEngine
import curses
from time import sleep


class BoardSelector:

    def __init__(self, board_controller: BoardController):
        self.graphic_engine = GraphicEngine()
        self.board_controller = board_controller
        self._current_cell = self.board_controller.board[0][0]
        main = Thread(target=self._run)
        main.start()

    # TODO: Board selector a finir.
    def _run(self):
        self._select(self._current_cell)
        while self.graphic_engine.key != 113:
            if self.graphic_engine.key == curses.KEY_RIGHT:
                self._select(self.board_controller.board[0][self._current_cell.x + 1])
                # On evite la duplication de touches
                sleep(0.1)


    def _select(self, cell):
        self._current_cell.selected = False
        cell.selected = True
        self._current_cell = cell
        self.graphic_engine.draw_board(self.board_controller)

