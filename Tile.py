# Module contains instructions for a single overworld tile object.
# A tile consists of a type of the tile, whether it is walkable, surfable,
# potential action when interacted with, whether or not there is a hidden item
# and whether the tile is a warp or not.

class Tile:
    def __init__(self, type: str, walkable:bool=True, surfable:bool=False,
                 interaction:str=None, hiddenitem:str=None, warp:str=None):
        self.__type = type
        self.__walkable = bool(int(walkable))
        self.__surfable = bool(int(surfable))
        self.__interaction = interaction
        self.__hiddenitem = hiddenitem
        if warp is not None:
            self.__warp = warp.split(":")

    def get_type(self) -> int:
        return self.__type

    def get_walkable(self) -> bool:
        return self.__walkable

    def get_surfable(self) -> bool:
        return self.__surfable

    def get_interaction(self):
        return self.__interaction

    def get_hiddenitem(self):
        return self.__hiddenitem

    def get_warp(self):
        return self.__warp

    def is_walkable(self):
        return self.get_walkable()

    def is_surfable(self):
        return self.get_surfable()

    def is_warp(self):
        return self.__warp is not None