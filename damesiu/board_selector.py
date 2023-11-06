from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from damesiu.objects import BoardController

from threading import Thread
from damesiu.helpers.singleton_patterns import SingletonThreadSafe
from damesiu.graphic_engine import Engine as GraphicEngine


class BoardSelector:

    def __init__(self, board_controller: BoardController):
        self.graphic_engine = GraphicEngine()
        self.board_controller = board_controller
