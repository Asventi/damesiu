from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import BoardController
    from damesiu.objects import Cell
    from damesiu.objects import Pion

import curses
from damesiu.graphic_engine.utils.colors import Colors
from threading import Thread
from damesiu.helpers.singleton_patterns import SingletonThreadSafe


class Engine(metaclass=SingletonThreadSafe):
    """
    La classe moteur graphique console pour le jeu
    """

    def __init__(self):
        """Initialistion basique du moteur graphique"""
        self._key = None
        self._colors = None
        self._screen = None
        main = Thread(target=self._start)
        main.start()

    def _start(self):
        """
        La fonction principale du moteur graphique
        """
        curses.wrapper(self._run)
        return 0

    def _run(self, screen):
        """
        La fonction principale du moteur graphique
        """
        self._colors = Colors(curses)
        self._screen = screen

        while self._key != 'q':
            self._screen.refresh()
            self._key = self._screen.getkey()

    def draw_board(self, board: BoardController):
        """
        Dessine le plateau de jeu
        """
        self._screen.addstr("-" * (board.size * 3) + "-" * 2)
        self._screen.addstr(11, 0, "-" * (board.size * 3) + "-" * 2)
        for i in range(board.size):
            self._screen.addstr(i + 1, 0, "|")
            self._screen.addstr(i + 1, board.size * 3 + 1, "|")

        for i in range(board.size):
            for j in range(board.size):
                self.draw_cell(board.board[i][j],
                               self._colors.cell_color_black if (i + j) % 2 == 0 else self._colors.cell_color_white)

    def draw_cell(self, cell: Cell, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(cell.y+1, cell.x * 3 + 1, ' ', color)
        if cell.pion is None:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, ' ', color)
        else:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', color)
        self._screen.addstr(cell.y+1, cell.x * 3 + 3, ' ', color)
