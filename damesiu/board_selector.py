from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import BoardController

from threading import Thread
from damesiu.graphic_engine import Engine as GraphicEngine
import curses


class BoardSelector:

    def __init__(self, board_controller: BoardController):
        self.graphic_engine = GraphicEngine()
        self.board_controller = board_controller
        main = Thread(target=self._run)
        main.start()

    def _run(self):
        while self.graphic_engine.key != 'q':
            if self.graphic_engine.key == 'KEY_UP':
                self.graphic_engine.add_message('test')
