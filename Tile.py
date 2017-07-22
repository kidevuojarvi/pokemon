class Tile:
    def __init__(self):
        self.__passable = False

    def is_passable(self):
        return self.__passable