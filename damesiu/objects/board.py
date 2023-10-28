from damesiu.objects.pion import Pion

class Board:
    def __init__(self):
        self.size = 10
        self.plateau = [[0 for i in range(10)] for i in range(10)]
        self.starter()
        print(self.plateau)

    def starter(self):
        for ligne in range(4):
            for colonne in range(0, 10, 2):
                self.plateau[ligne][colonne + (1 if ligne % 2 == 0 else 0)] = Pion(ligne, colonne + 1 if ligne % 2 == 0 else 0, "blanc")
                self.plateau[self.size - ligne - 1][colonne + (1 if ligne % 2 == 0 else 0)] = Pion(self.size - ligne, colonne + 1 if ligne % 2 == 0 else 0, "noir")
