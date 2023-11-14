from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import BoardController
    from damesiu.objects import Cell

from threading import Thread
from damesiu.graphic_engine import Engine as GraphicEngine
import curses
from time import sleep


class BoardSelector:

    def __init__(self, board_controller: BoardController):
        self.graphic_engine = GraphicEngine()
        self.board_controller = board_controller
        self._current_cell = self.board_controller.board[0][0]
        self._selected_cell: Cell | None = None
        main = Thread(target=self._run)
        main.start()


    def _run(self):
        self._highlight(self._current_cell)
        while self.graphic_engine.key != 113:
            if self.graphic_engine.key == curses.KEY_UP and self._current_cell.y - 1 >= 0:
                self._highlight(self.board_controller.board[self._current_cell.y - 1][self._current_cell.x])
                # On evite la duplication de touches
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_LEFT and self._current_cell.x - 1 >= 0:
                self._highlight(self.board_controller.board[self._current_cell.y][self._current_cell.x - 1])
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_DOWN and self._current_cell.y + 1 < self.board_controller.size:
                self._highlight(self.board_controller.board[self._current_cell.y + 1][self._current_cell.x])
                sleep(0.1)

            elif self.graphic_engine.key == curses.KEY_RIGHT and self._current_cell.x + 1 < self.board_controller.size:
                self._highlight(self.board_controller.board[self._current_cell.y][self._current_cell.x + 1])
                sleep(0.1)

            elif self.graphic_engine.key == 10:
                self._select()
                sleep(0.1)

    def _highlight(self, cell):
        self._current_cell.highlighted = False
        cell.highlighted = True
        self._current_cell = cell
        self.update()

    def _select(self):

        if self._current_cell == self._selected_cell:
            self._selected_cell.selected = False
            self._selected_cell = None
        else:
            # On deselectionne l'ancienne cell selectionne et on enleve l'highlight
            if self._selected_cell is not None:
                self._selected_cell.selected = False
            self._current_cell.highlighted = False

            # On selectionne la cell et on la stock
            self._selected_cell = self._current_cell
            self._selected_cell.selected = True

        # On met a jour le board
        self.update()

    def update(self):
        self.graphic_engine.draw_board(self.board_controller)