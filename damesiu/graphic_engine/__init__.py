import curses
import asyncio
from damesiu.graphic_engine.utils.colors import Colors

class GraphicEngine:
    """
    La classe moteur graphique console pour le jeu
    """
    def __init__(self):
        """Initialistion basique du moteur graphique"""
        self._key = None
        self._colors = None
        self._screen = None

    def start(self):
        """
        La fonction principale du moteur graphique
        """
        curses.wrapper(asyncio.run(self.run()))

        return 0

    async def run(self, screen):
        """
        La fonction principale du moteur graphique
        """
        curses.wrapper(self.run)
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

    def draw_cell(self, x, y, color):
        """
        Dessine une cellule a la position x, y
        """
        self._screen.addstr(y, x*4, ' ', color)
        self._screen.addstr(y, x*4+1, ' ', color)
        self._screen.addstr(y, x*4+2, ' ', color)
        self._screen.addstr(y, x*4+3, '', self._colors.cell_color_black)
        pass

