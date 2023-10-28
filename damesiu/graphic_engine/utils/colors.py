
class Colors:

    def __init__(self, curses):
        """
        Initialisation des couleurs
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
        self.cell_color_black = curses.color_pair(1)
        self.cell_color_white = curses.color_pair(2)

