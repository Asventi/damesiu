class Pion:
    def __init__(self, x, y, couleur):
        self.ligne = x
        self.colonne = y
        self.couleur = couleur
class Reine:
    def __init__(self, x, y, couleur):
        self.ligne = x
        self.colonne = y
        self.couleur = couleur

class Plateau:
    def __init__(self):
        self.size = 10
        self.plateau = None
        self.starter()

    def starter(self):
        for ligne in range(3):
            for colonne in range(0, 10, 2):
                self.plateau[ligne][colonne] = Pion(ligne, colonne, "blanc")
        for ligne in range(3):
            for colonne in range(0, 10, 2):
                self.plateau[self.size - ligne][colonne] = Pion(self.size - ligne, colonne, "noir")
    def retour_plateau(self):
        for ligne in self.plateau:
            for case in ligne:
                if case is None:
                    print("caca")
                else:
                    print("gros caca")
