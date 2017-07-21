from Pokemon import Pokemon
# TODO: Import everything

# Singleton
class Game:
    def __init__(self):
        self.__state = None # Cutscene, overworld, combat
        self.__area = None # Area of the map currently displayed
        