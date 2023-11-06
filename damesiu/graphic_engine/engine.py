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
import time


class Engine(metaclass=SingletonThreadSafe):
    """
    La classe moteur graphique console pour le jeu
    """

    def __init__(self):
        """Initialistion basique du moteur graphique"""
        self._key = None
        self._colors: Colors | None = None
        self._screen = None
        main = Thread(target=curses.wrapper, args=(self._run,))
        main.start()

    def _run(self, screen):
        """
        La fonction principale du moteur graphique
        """
        self._colors = Colors(curses)
        self._screen = screen
        curses.curs_set(False)

        while self._key != 'q':
            self._key = self._screen.getkey()
            time.sleep(0.1)

    def draw_board(self, board: BoardController):
        """
        Dessine le plateau de jeu
        """

        self._screen.addstr("-" * (board.size * 3) + "-" * 2)
        self._screen.addstr(board.size + 1, 0, "-" * (board.size * 3) + "-" * 2)
        for i in range(board.size):
            self._screen.addstr(i + 1, 0, "|")
            self._screen.addstr(i + 1, board.size * 3 + 1, "|")

        for i in range(board.size):
            for j in range(board.size):
                self.draw_cell(board.board[i][j],
                               self._colors.blackcell if (i + j) % 2 == 0 else self._colors.whitecell)
        self._screen.refresh()

    def draw_cell(self, cell: Cell, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(cell.y + 1, cell.x * 3 + 1, ' ', color)
        self._screen.addstr(cell.y + 1, cell.x * 3 + 3, ' ', color)

        if cell.pion is not None:
            if color is self._colors.whitecell:
                if cell.pion.color == "blanc":
                    self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.whitecell_whitepion)
                else:
                    self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.whitecell_blackpion)
            else:
                if cell.pion.color == "blanc":
                    self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.blackcell_whitepion)
                else:
                    self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.blackcell_blackpion)

        else:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, ' ', color)

    def add_message(self, message: str):
        self._screen.addstr(5, 45, message)
        # Fonction pour clear le rest de la ligne pour enlever l'ancien message
        self._screen.clrtoeol()
        self._screen.refresh()

    @property
    def key(self):
        return self._key
