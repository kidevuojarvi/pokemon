from GUI import GUI
from Area import Area
# TODO: Import everything

# Singleton
class Game:
    def __init__(self):
        self.__state = None # Cutscene, overworld, combat
        self.__area = None # Area of the map currently displayed
        self.__map = Area(0)
        self.__UI = GUI(self)


    def is_passable(self, x, y):
        return self.__map.is_passable(x, y)

    def get_map(self):
        return self.__map