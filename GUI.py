from tkinter import *
from time import time, sleep
from random import randint

WIDTH = 128
HEIGHT = 128

class GUI:
    def __init__(self, world):
        self.__mw = Tk()
        self.__mw.title("Pokemon")

        self.__parent = world

        self.__red_image = PhotoImage(file="./data/images/red.png")
        self.__block_image = PhotoImage(file="./data/images/block.png")
        self.__tree_image = PhotoImage(file="./data/images/tree.png")
        self.__white_image = PhotoImage(file="./data/images/white.png")
        self.__warp_image = PhotoImage(file="./data/images/warp.png")

        self.__canvas = Canvas(self.__mw, width=WIDTH, height=HEIGHT)
        self.__canvas.pack(expand=1, fill=BOTH)

        self.__x = 4
        self.__y = 4

        self.__blocks = []
        map = self.__parent.get_map().get_map()
        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                if tile.get_type() == "block":
                    self.__blocks.append(self.__canvas.create_image(16 * i + 8, 16 * j + 8, image=self.__block_image))
                elif tile.get_type() == "tree":
                    self.__blocks.append(self.__canvas.create_image(16 * i + 8, 16 * j + 8, image=self.__tree_image))
                elif tile.get_type() == "warp":
                    self.__blocks.append(self.__canvas.create_image(16 * i + 8, 16 * j + 8, image=self.__warp_image))
                else:
                    self.__blocks.append(self.__canvas.create_image(16 * i + 8, 16 * j + 8, image=self.__white_image))
        self.__red = self.__canvas.create_image(self.__x * 16 + 8, self.__y * 16 + 8, image=self.__red_image)

        self.__num = 0
        self.__numlbl = Label(self.__mw, text="0")
        self.__numlbl.pack()

        self.__mw.bind("<KeyPress>", self.key_event)

        self.__mw.after(10, self.ticker)
        self.__mw.mainloop()


    def key_event(self, event):
        if event.keysym == "Escape":
            self.__mw.destroy()

        elif event.keysym == "Up":
            if self.__parent.is_passable(self.__x, self.__y - 1):
                self.__y -= 1
                for block in self.__blocks:
                    self.__canvas.move(block, 0, 16)
            else:
                print("Bump")
                #TODO: bump-sound

        elif event.keysym == "Down":
            if self.__parent.is_passable(self.__x, self.__y + 1):
                self.__y += 1
                for block in self.__blocks:
                    self.__canvas.move(block, 0, -16)
            else:
                print("Bump")
                #TODO: bump-sound


        elif event.keysym == "Right":
            if self.__parent.is_passable(self.__x + 1, self.__y):
                self.__x += 1
                for block in self.__blocks:
                    self.__canvas.move(block, -16, 0)
            else:
                print("Bump")
                #TODO: bump-sound

        elif event.keysym == "Left":
            if self.__parent.is_passable(self.__x - 1, self.__y):
                self.__x -= 1
                for block in self.__blocks:
                    self.__canvas.move(block, 16, 0)
            else:
                print("Bump")
                #TODO: bump-sound

        if self.__parent.get_map().is_warp(self.__x, self.__y):
            new = self.__parent.get_map().get_tile(self.__x, self.__y).get_warp().split(":")
            self.__x = int(new[1])
            self.__y = int(new[2])
            # TODO: Refocus the camera!!!



    def ticker(self):
        self.up()
        self.__mw.after(10, self.ticker)

    def up(self):
        self.__num += 0.01
        self.__numlbl["text"] = "{:.2f}".format(self.__num)

    def down(self):
        self.__num -= 1
        self.__numlbl["text"] = str(self.__num)




#def main():
#    GUI()


#main()