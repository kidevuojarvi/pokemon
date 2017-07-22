from Pokemon import Pokemon
from GUI import GUI
# TODO: Import everything

# Singleton
class Game:
    def __init__(self):
        self.__state = None # Cutscene, overworld, combat
        self.__area = None # Area of the map currently displayed
        self.__map = []
        self.__UI = GUI(self)


    def is_passable(self, x, y):
        return self.__map[y][x].is_passable()