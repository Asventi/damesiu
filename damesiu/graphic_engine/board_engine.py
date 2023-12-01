from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from damesiu.controllers.board_controller import BoardController
    from damesiu.objects import Cell
import curses
from damesiu.graphic_engine.utils.colors import Colors
from threading import Thread
from threading import Lock
from damesiu.utils import EventHandler



class GraphicEngineSingleton(type):
    """
    Thread safe singleton pour le moteur graphique, permet d'eviter d'avoir plusieurs instance du moteur graphique
    et d'avoir la meme a chaque appel
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


class BoardEngine(EventHandler, metaclass=GraphicEngineSingleton):
    """
    La classe moteur graphique console pour le jeu
    """

    def __init__(self) -> None:
        """Initialistion basique du moteur graphique"""
        self._key: Optional[int] = None
        main = Thread(target=curses.wrapper, args=(self._run,))
        main.start()

    def _run(self, screen) -> None:
        """
        La fonction principale du moteur graphique screen est renvoyé par curses.wrapper
        """
        # Initialisation des couleurs pour le terminal
        self._colors: Colors = Colors(curses)
        self._screen = screen
        curses.curs_set(False)
        self._screen.nodelay(True)
        # Verification de la taille de la fenetre
        y, x = self._screen.getmaxyx()
        while y < 12 or x < 102:
            self._screen.addstr(0, 0, f"La taille de la fenetre doit etre de 102x12, taille actuelle : {x} {y}")
            self._screen.refresh()
            y, x = self._screen.getmaxyx()

        # Boucle qui garde le moteur graphique en vie et gere les evenements clavier
        while self._key != 113:
            try:
                self._key = self._screen.getch()
                if self._key != -1:
                    self.trigger("key_pressed", key=self._key)

            except curses.ERR:
                self._key = None
        curses.endwin()

    def draw_board(self, board: BoardController) -> None:
        """
        Dessine le plateau de jeu a partir du board controller

        :param board: Board controller
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

    def draw_cell(self, cell: Cell, color: str) -> None:
        """
        Dessine une cellule en fonction de sa position y x et l'adapte aux coordonnées du terminal

        :param cell: Cellule a dessiner
        :param color: Couleur de la cellule : "black" ou "white"
        :raises ValueError: Si la couleur n'est pas "black" ou "white"
        """
        if color not in ["black", "white", "highlighted", "selected"]:
            raise ValueError("Color must be black, white, highlighted or selected")

        self._screen.addstr(cell.y + 1, cell.x * 3 + 1, ' ', self._colors.get_color_pair(color))
        self._screen.addstr(cell.y + 1, cell.x * 3 + 3, ' ', self._colors.get_color_pair(color))

        if cell.pion is not None:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, 'o', self._colors.get_color_pair(color, cell.pion.color))
        elif cell.playable:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, '°', self._colors.get_color_pair(color, "playable"))
        else:
            self._screen.addstr(cell.y + 1, cell.x * 3 + 2, ' ', self._colors.get_color_pair(color))

    def add_message(self, message: Any) -> None:
        """
        Ajoute un message dans la zone de message du moteur graphique, cast automatiquement le message en string

        :param message: Message a afficher
        """
        if message is not None:
            self._screen.addstr(5, 35, str(message))
            # Fonction pour clear le rest de la ligne pour enlever l'ancien message
            self._screen.clrtoeol()
            self._screen.refresh()

    def add_alert(self, message: Any):
        """
        Ajoute un message dans la zone d'alerte du moteur graphique, cast automatiquement le message en string

        :param message: Message a afficher
        """
        if message is not None:
            self._screen.addstr(6, 35, str(message))
            # Fonction pour clear le rest de la ligne pour enlever l'ancien message
            self._screen.clrtoeol()
            self._screen.refresh()

    def clear_alert(self) -> None:
        """
        Efface le message d'alerte utile pour pas que le message d'alerte reste affiché en permanence
        """
        self._screen.addstr(6, 35, " ")
        self._screen.clrtoeol()
        self._screen.refresh()

    def set_score(self, score: int, name: str, y: int) -> None:
        """
        Affiche le score d'un joueur, y est le playercode du joueur, ca sert a savoir ou afficher le score

        :param score: Score du joueur
        :param name: Nom du joueur
        :param y: Playercode du joueur
        """
        self._screen.addstr(0 + y, 35, f"{name} : {score}")
        self._screen.clrtoeol()
        self._screen.refresh()

    @property
    def key(self):
        return self._key

    def __del__(self):
        curses.endwin()
