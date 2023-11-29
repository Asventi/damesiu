from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from damesiu.objects import Player, Cell
    from damesiu.objects import Cell

from damesiu.constants import directions


class Pion:
    def __init__(self, x: int, y: int, color: str, cell: Cell, player: Player):
        self.ligne = x
        self.colonne = y
        self.color = color
        self.player = player

        self.cell = cell
        self.queen: bool = False

    def get_playable_cells(self, direction: str = None, only_eat: bool = False) -> list[Cell]:
        if direction is None:
            direction = directions.N if self.color == 'black' else directions.S
        playable_cells = []

        if direction == 'all':
            if self.get_playable_cell(directions.NE, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.NE, True))

            if self.get_playable_cell(directions.SE, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.SE, True))

            if self.get_playable_cell(directions.NW, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.NW, True))

            if self.get_playable_cell(directions.SW, True) is not None:
                playable_cells.append(self.get_playable_cell(directions.SW, True))

        else:
            if self.get_playable_cell(direction - 1, only_eat=only_eat) is not None:
                playable_cells.append(self.get_playable_cell(direction - 1, only_eat=only_eat))

            if self.get_playable_cell(direction + 1, only_eat=only_eat) is not None:
                playable_cells.append(self.get_playable_cell(direction + 1, only_eat=only_eat))

        return playable_cells

    def get_playable_cell(self, direction, only_eat: bool = False) -> Cell | None:
        neighbor = self.cell.neighbors[direction]

        if neighbor is not None:
            if neighbor.pion is not None:
                if neighbor.pion.color != self.color:
                    neighbor_eat = neighbor.pion.cell.neighbors[direction]
                    if neighbor_eat is not None and neighbor_eat.pion is None:
                        return neighbor_eat
            elif not only_eat:
                return neighbor
        return None

    def __repr__(self):
        return f"Pion({self.ligne}, {self.colonne}, {self.color}, {self.cell}, {self.player})"
