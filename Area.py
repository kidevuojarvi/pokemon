from readdata import AREADATA
from Tile import Tile

class Area:
    def __init__(self, id_num: int, flyable: bool = True, cycleable: bool = True):
        self.__id = id_num
        self.__map = []
        self.__flyable = flyable
        self.__cycleable = cycleable

        self.create_area()


    def create_area(self):
        data = AREADATA[self.__id]
        i = 0
        tileinfo = {}
        while data[i] != "MAP" and i <= len(data):
            row = data[i].split("=")
            tileinfo[row[0]] = row[1].split(",")
            i += 1
        i += 1
        while i < len(data):
            row = []
            for char in data[i]:
                if char in tileinfo:
                    tile = Tile(*tileinfo[char])
                else:
                    tile = Tile(*tileinfo["neutral"])
                row.append(tile)
            self.__map.append(row)
            i += 1

    def is_passable(self, x, y):
        return self.__map[y][x].is_walkable()

    def is_warp(self, x, y):
        return self.__map[y][x].is_warp()

    def get_tile(self, x, y):
        return self.__map[y][x]

    def get_map(self):
        return self.__map

"""
0,0   0,1
1,0   1,1


"""