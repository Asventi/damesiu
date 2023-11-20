
class Colors:

    def __init__(self, curses):
        """
        Initialisation des couleurs
        """
        curses.start_color()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.whitecell_whitepion = curses.color_pair(1)
        self.whitecell_blackpion = curses.color_pair(2)
        self.blackcell_whitepion = curses.color_pair(3)
        self.blackcell_blackpion = curses.color_pair(4)
        self.whitecell = curses.color_pair(1)
        self.blackcell = curses.color_pair(3)

        self.highlightedcell = curses.color_pair(5)
        self.highlightedcell_whitepion = curses.color_pair(5)
        self.highlightedcell_blackpion = curses.color_pair(6)

        self.selectedcell = curses.color_pair(7)
        self.selectedcell_whitepion = curses.color_pair(7)
        self.selectedcell_blackpion = curses.color_pair(8)

        self.whitecell_playable = curses.color_pair(9)
        self.blackcell_playable = curses.color_pair(10)



