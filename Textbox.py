from tkinter import *

class Textbox:
    def __init__(self, text:str="", border:int=0, speed:int=0):
        self.__text = text
        self.__border = border
        self.__speed = speed
        self.__line_finished = True

    @property
    def line_finished(self) -> bool:
        return self.__line_finished

    def next_line(self):
        pass

    def empty_box(self):
        pass

    def create_box(self):
        pass

