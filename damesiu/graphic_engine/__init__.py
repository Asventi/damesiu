import curses
from damesiu.graphic_engine.utils.colors import Colors
import threading

class GraphicEngine:
    """
    La classe moteur graphique console pour le jeu
    """
    def __init__(self):
        """Initialistion basique du moteur graphique"""
        self._key = None
        self._colors = None
        self._screen = None
        main = threading.Thread(target=self._start)
        main.start()

    def _start(self):
        """
        La fonction principale du moteur graphique
        """
        curses.wrapper(self.run)
        return 0

    def run(self, screen):
        """
        La fonction principale du moteur graphique
        """
        self._colors = Colors(curses)
        self._screen = screen

        self.draw_board(10)
        print(curses.COLS)

        while self._key != 'q':
            self._screen.refresh()
            self._key = self._screen.getkey()

    def draw_board(self, size):
        """
        Dessine le plateau de jeu
        """
        for i in range(size):
            for j in range(size):
                self.draw_cell(j, i, self._colors.cell_color_white)
        pass

    def print(self, string):
        """
        Affiche une chaine de caractere a la position x, y
        """
        self._screen.addstr(string)
        pass

    def draw_cell(self, x, y, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(y, x*4, ' ', color)
        self._screen.addstr(y, x*4+1, ' ', color)
        self._screen.addstr(y, x*4+2, ' ', color)
        self._screen.addstr(y, x*4+3, '', self._colors.cell_color_black)
        pass

