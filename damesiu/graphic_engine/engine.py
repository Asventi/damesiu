import curses
from damesiu.graphic_engine.utils.colors import Colors
from threading import Thread, Lock


class SingletonMeta(type):
    """
    Thread safe singleton metaclass
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


class Engine(metaclass=SingletonMeta):
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
        self.draw_board(10)

        while self._key != 'q':
            self._screen.refresh()
            self._key = self._screen.getkey()

    def draw_board(self, size):
        """
        Dessine le plateau de jeu
        """
        self._screen.addstr("-" * (size * 3) + "-" * 2)
        self._screen.addstr(11, 0, "-" * (size * 3) + "-" * 2)
        for i in range(size):
            self._screen.addstr(i + 1, 0, "|")
            self._screen.addstr(i + 1, size * 3 + 1, "|")

        for i in range(size):
            for j in range(size):
                self.draw_cell(j, i + 1,
                               self._colors.cell_color_black if (i + j) % 2 == 0 else self._colors.cell_color_white)

    def draw_cell(self, x, y, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(y, x * 3 + 1, ' ', color)
        self._screen.addstr(y, x * 3 + 2, 'o', color)
        self._screen.addstr(y, x * 3 + 3, ' ', color)
