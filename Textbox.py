from tkinter import *
from Box import Box

class Textbox(Box):
    def __init__(self, canvas:Canvas, text:str="", zoom:int=1, border:int=0, speed:int=0):
        Box.__init__(self, canvas, (0, 6), (9, 8), zoom, border)
        self.__text = text
        self.__speed = speed
        self.__line_finished = True


    @property
    def line_finished(self) -> bool:
        return self.__line_finished

    def next_line(self, canvas):
        pass

    def empty_box(self, canvas):
        pass
