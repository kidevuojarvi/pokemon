# Singleton
class Walk_animation:
    def __init__(self):
        self.__current = 0
        self.__previous = True
        self.__direction = "down"
        self.__movement = False

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def next_frame(self):
        self.__movement = not self.__movement
        if self.__movement:
            self.__previous = not self.__previous
            walkstring = "walk_" + self.__direction
            if not self.__previous or self.__direction in ["left", "right"]:
                return walkstring
            else:
                return walkstring + "_l"

        else:
            return self.__direction