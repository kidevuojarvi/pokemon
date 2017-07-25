from GUI import GUI
from Area import Area
# TODO: Import everything

# Singleton
class Game:
    def __init__(self):
        self.__state = None # Cutscene, overworld, combat
        self.__area = 0 # Area of the map currently displayed
        self.__map = Area(0)
        self.__UI = GUI(self)


    def is_passable(self, x, y):
        return self.__map.is_passable(x, y)

    def get_map(self):
        return self.__map

    def warp(self, new_area):
        # Don't recreate if warped to the same map
        if self.__area == new_area:
            return
        self.__area = new_area
        self.__map = Area(new_area)