from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player

from .cell import Cell
from .pion import Pion
from damesiu.graphic_engine import Engine as GraphicEngine


class BoardController:
    def __init__(self, players: list[Player], size: int = 10):
        self._players = players
        self._size = size

        self.board: list[list[Cell]] = []
        self.graphic_engine = GraphicEngine()

        self.starter()

    def starter(self):
        self.create_board()
        self.add_pions()
        self.graphic_engine.draw_board(self)


    def create_board(self):
        if len(self.board) > 0:
            self.board = []

        for y in range(self._size):
            self.board.append([])
            for x in range(self._size):
                self.board[y].append(Cell(x, y))
    def add_pions(self):
        for y in range(4):
            for x in range(self._size):
                if (x + y) % 2 == 0:
                    # TODO: Ajouter les pions a la liste de pion du player
                    self.board[y][x-1].pion = Pion(y, x-1, "blanc", self.players[0])
                    self.board[self._size-y-1][x].pion = Pion(self._size-y-1, x, "noir", self.players[1])

    # Propertys
    @property
    def size(self):
        return self._size

    @property
    def players(self):
        return self._players
