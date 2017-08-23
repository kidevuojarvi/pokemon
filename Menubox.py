from tkinter import *
from Box import Box

class Menubox(Box):
    def __init__(self, canvas:Canvas, zoom:int=1, border:int=0):
        Box.__init__(self, canvas, (5, 0), (9, 8), zoom, border)
        Box.__init__(self, canvas, (0, 1), (3, 3), zoom, border)
        self.__items = []

    def show_item(self, item):
        pass

    def hide_item(self, item):
        pass

    def update(self):
        pass

