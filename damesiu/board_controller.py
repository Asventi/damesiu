from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player

from damesiu.objects import Cell
from damesiu.objects import Pion
from damesiu.graphic_engine import Engine as GraphicEngine
from damesiu.board_selector import BoardSelector
import time
from damesiu.constants import directions

class BoardController:
    def __init__(self, players: list[Player], size: int = 10):
        self._players = players
        self._size = size

        self.board: list[list[Cell]] = []
        self.graphic_engine = GraphicEngine()

        self.starter()

        self.board_selector = BoardSelector(self)

    def starter(self):
        self.create_board()
        self.add_pions()
        self.graphic_engine.draw_board(self)

    def create_board(self):
        if len(self.board) > 0:
            self.board = []

        # TODO: Ajouter les voisins de la Cell a chaque creation
        for y in range(self._size):
            self.board.append([])
            for x in range(self._size):
                self.board[y].append(Cell(x, y))


    def add_pions(self):
        pions_count = int(self._size / 2 - 1)
        for y in range(pions_count):
            for x in range(self._size):
                if (x + y) % 2 == 0:
                    pion1 = Pion(y, x - 1, "white", self.board[y][x - 1], self.players[0])
                    self.board[y][x - 1].pion = pion1
                    self._players[0].pions.append(pion1)

                    pion2 = Pion(self._size - y - 1, x, "black", self.board[self._size - y - 1][x], self.players[1])
                    self.board[self._size - y - 1][x].pion = pion2
                    self._players[1].pions.append(pion2)
        self.set_board_neighbors()

    # TODO: Finir cette fonction qui devra retourner une liste de cellule jouable selon le joueur entre (la mort ptn)
    def get_playable_cells(self, pion: Pion, player: Player):
        pass

    def set_board_neighbors(self):
        for y in range(self._size):
            for cell in self.board[y]:
                for i in range(3):
                    if 0 <= cell.x + i - 1 < self._size and y != 0:
                        neighbor = self.board[y - 1][cell.x + i - 1]
                        cell.neighbors.append(neighbor)
                    else:
                        cell.neighbors.append(None)

                if cell.x + 1 < self._size:
                    neighbor = self.board[y][cell.x + 1]
                    cell.neighbors.append(neighbor)
                else:
                    cell.neighbors.append(None)

                if y != self._size - 1:
                    for i in range(3):
                        if 0 <= cell.x - i + 1 < self._size:
                            neighbor = self.board[y + 1][cell.x - i + 1]
                            cell.neighbors.append(neighbor)
                        else:
                            cell.neighbors.append(None)

                if cell.x - 1 >= 0:
                    neighbor = self.board[y][cell.x - 1]
                    cell.neighbors.append(neighbor)
                else:
                    cell.neighbors.append(None)



    # Propertys
    @property
    def size(self):
        return self._size

    @property
    def players(self):
        return self._players
