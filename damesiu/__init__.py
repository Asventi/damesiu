from damesiu.graphic_engine import GraphicEngine


def run():
    """
    La fonction principale du jeu
    """
    engine = GraphicEngine()

    plateau = [[0 for i in range(10)] for j in range(10)]
    print(plateau)
