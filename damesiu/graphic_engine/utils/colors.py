
class Colors:

    def __init__(self, curses):
        """
        Initialisation des couleurs
        """
        curses.start_color()

        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_GREEN)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_RED)

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
        self.highlightedcell_playable = curses.color_pair(11)

    def get_color_pair(self, cell_color: str, pion_color: str = 'white') -> int:
        """
        Renvoie le code couleur en fonction de la couleur de la cellule et du pion

        :param cell_color: Couleur de la cellule
        :param pion_color: Couleur du pion
        :return: Code couleur
        :rtype: int
        """
        if cell_color == "highlighted":
            if pion_color == "playable":
                return self.highlightedcell_playable
            elif pion_color == "white":
                return self.highlightedcell_whitepion
            else:
                return self.highlightedcell_blackpion
        elif cell_color == "selected":
            if pion_color == "white":
                return self.selectedcell_whitepion
            else:
                return self.selectedcell_blackpion
        elif cell_color == "white":
            if pion_color == "playable":
                return self.whitecell_playable
            elif pion_color == "white":
                return self.whitecell_whitepion
            else:
                return self.whitecell_blackpion
        else:
            if pion_color == "playable":
                return self.blackcell_playable
            elif pion_color == "white":
                return self.blackcell_whitepion
            else:
                return self.blackcell_blackpion
