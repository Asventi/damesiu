from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.controllers.board_controller import BoardController
    from damesiu.objects import Cell
import curses
from damesiu.graphic_engine.utils.colors import Colors
from threading import Thread
from threading import Lock
from time import sleep


class GraphicEngineSingleton(type):
    """
    Thread safe singleton for Graphic Engine
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


class Engine(EventHandler, metaclass=GraphicEngineSingleton):
    """
    La classe moteur graphique console pour le jeu
    """

    def __init__(self):
        """Initialistion basique du moteur graphique"""
        self._key: int | None = None
        main = Thread(target=curses.wrapper, args=(self._run,))
        main.start()

    def _run(self, screen):
        """
        La fonction principale du moteur graphique
        """
        self._colors = Colors(curses)
        self._screen = screen
        curses.curs_set(False)
        self._screen.nodelay(True)

        while self._key != 113:
            try:
                self._key = self._screen.getch()
                if self._key != -1:
                    self.trigger("key_pressed", key=self._key)

            except curses.ERR:
                self._key = None

    def draw_board(self, board: BoardController):
        """
        Dessine le plateau de jeu
        """

        self._screen.addstr(0, 0, "-" * (board.size * 3) + "-" * 2)
        self._screen.addstr(board.size + 1, 0, "-" * (board.size * 3) + "-" * 2)
        for i in range(board.size):
            self._screen.addstr(i + 1, 0, "|")
            self._screen.addstr(i + 1, board.size * 3 + 1, "|")

        for i in range(board.size):
            for j in range(board.size):
                cell = board.board[i][j]
                if cell.highlighted:
                    self.draw_cell(cell, "highlighted")
                elif cell.selected:
                    self.draw_cell(cell, "selected")
                else:
                    self.draw_cell(cell, "black" if (i + j) % 2 == 0 else "white")
        self._screen.refresh()

    def draw_cell(self, cell: Cell, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(cell.y + 1, cell.x * 3 + 1, ' ', self._colors.get_color_pair(color))
        self._screen.addstr(cell.y + 1, cell.x * 3 + 3, ' ', self._colors.get_color_pair(color))

        if cell.pion is not None:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.get_color_pair(color, cell.pion.color))
        elif cell.playable:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, '°', self._colors.get_color_pair(color, "playable"))
        else:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, ' ', self._colors.get_color_pair(color))

    def add_message(self, message):
        if message is not None:
            self._screen.addstr(5, 35, str(message))
            # Fonction pour clear le rest de la ligne pour enlever l'ancien message
            self._screen.clrtoeol()
            self._screen.refresh()

    def add_alert(self, message):
        if message is not None:
            self._screen.addstr(6, 35, str(message))
            # Fonction pour clear le rest de la ligne pour enlever l'ancien message
            self._screen.clrtoeol()
            self._screen.refresh()

    def clear_alert(self):
        self._screen.addstr(6, 35, " ")
        self._screen.clrtoeol()
        self._screen.refresh()

    @property
    def key(self):
        return self._key
