from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import Player
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

    def get_playable_cells(self) -> list[Cell]:
        neighbors = self.cell.neighbors
        direction = directions.N if self.color == 'black' else directions.S
        neighbor_w = neighbors[direction + 1]
        neighbor_e = neighbors[direction - 1]
        playable_cells = []

        if neighbor_w is not None:
            if neighbor_w.pion is not None:
                # TODO: Logique si il y a un pion pour verifier derriere si on peut bouffer sa grand mere la pute
                pass
            else:
                playable_cells.append(neighbor_w)

        if neighbor_e is not None:
            if neighbor_e.pion is not None:
                # TODO: Logique si il y a un pion pour verifier derriere si on peut bouffer sa grand mere la pute
                pass
            else:
                playable_cells.append(neighbor_e)


        return playable_cells

    def __repr__(self):
        return f"Pion({self.ligne}, {self.colonne}, {self.color}, {self.cell}, {self.player})"
