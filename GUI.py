from tkinter import *
from time import time, sleep
from random import randint

ZOOM = 3
# Gameboy Screen is 10x9 tiles, and the player recides at 4, 4 while the world moves
# The overworld sprites are 16x16 pixels, so width and height are hardcoded, then
# adjusted with the ZOOM-factor
WIDTH = 160 * ZOOM
HEIGHT = 144 * ZOOM

class GUI:
    def __init__(self, world):
        self.__mw = Tk()
        self.__mw.title("Pokemon")

        self.__parent = world

        self.__ow_sprites = {"red": PhotoImage(file="./data/images/red.png").zoom(ZOOM, ZOOM),
                             "up": PhotoImage(file="./data/images/trainer/trainer_up.png").zoom(ZOOM, ZOOM),
                             "down": PhotoImage(file="./data/images/trainer/trainer_down.png").zoom(ZOOM, ZOOM),
                             "right": PhotoImage(file="./data/images/trainer/trainer_right.png").zoom(ZOOM, ZOOM),
                             "left": PhotoImage(file="./data/images/trainer/trainer_left.png").zoom(ZOOM, ZOOM),
                             "walk_up": PhotoImage(file="./data/images/trainer/trainer_up_walk.png").zoom(ZOOM, ZOOM),
                             "walk_down": PhotoImage(file="./data/images/trainer/trainer_down_walk.png").zoom(ZOOM, ZOOM),
                             "walk_right": PhotoImage(file="./data/images/trainer/trainer_right_walk.png").zoom(ZOOM, ZOOM),
                             "walk_left": PhotoImage(file="./data/images/trainer/trainer_left_walk.png").zoom(ZOOM, ZOOM),
                             "block": PhotoImage(file="./data/images/block.png").zoom(ZOOM, ZOOM),
                             "tree": PhotoImage(file="./data/images/tree.png").zoom(ZOOM, ZOOM),
                             "white": PhotoImage(file="./data/images/white.png").zoom(ZOOM, ZOOM),
                             "warp": PhotoImage(file="./data/images/warp.png").zoom(ZOOM, ZOOM)
                            }

        self.__canvas = Canvas(self.__mw, width=WIDTH, height=HEIGHT)
        self.__canvas.pack(expand=1, fill=BOTH)

        self.__ongoing_animation = False
        self.__prev_command = None
        self.__prev_command_timestamp = time()

        self.__x = 4
        self.__y = 4

        self.__blocks = []
        self.refocus()

        self.__num = 0
        self.__numlbl = Label(self.__mw, text="0")
        self.__numlbl.pack()

        self.__mw.bind("<KeyPress>", self.key_event)

        self.__mw.after(10, self.ticker)
        self.__mw.mainloop()


    def key_event(self, event):
        # TODO: Consider running and cycling
        if time() - self.__prev_command_timestamp < 0.3 and self.__prev_command == event.keysym:
            return

        if self.__ongoing_animation:
            return

        self.__prev_command = event.keysym
        self.__prev_command_timestamp = time()

        if event.keysym == "Escape":
            self.__mw.destroy()

        elif event.keysym == "Up":
            self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["up"])
            if self.__parent.is_passable(self.__x, self.__y - 1):
                self.__y -= 1
                self.movement_animation(0, 1, "up")
            else:
                print("Bump")
                #TODO: bump-sound

        elif event.keysym == "Down":
            self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["down"])
            if self.__parent.is_passable(self.__x, self.__y + 1):
                self.__y += 1
                self.movement_animation(0, -1, "down")
            else:
                print("Bump")
                #TODO: bump-sound


        elif event.keysym == "Right":
            self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["right"])
            if self.__parent.is_passable(self.__x + 1, self.__y):
                self.__x += 1
                self.movement_animation(-1, 0, "right")
            else:
                print("Bump")
                #TODO: bump-sound

        elif event.keysym == "Left":
            self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites["left"])
            if self.__parent.is_passable(self.__x - 1, self.__y):
                self.__x -= 1
                self.movement_animation(1, 0,"left")
            else:
                print("Bump")
                #TODO: bump-sound

        if self.__parent.get_map().is_warp(self.__x, self.__y):
            new = self.__parent.get_map().get_tile(self.__x, self.__y).get_warp()
            self.__parent.warp(int(new[0]))
            self.__x = int(new[1])
            self.__y = int(new[2])
            self.refocus()

    def refocus(self):
        delta_x = self.__x - 4
        delta_y = self.__y - 4
        print(self.__x, self.__y, delta_x, delta_y)
        self.__canvas.delete(ALL)
        self.__blocks = []
        map = self.__parent.get_map().get_map()
        for i, row in enumerate(map):
            for j, tile in enumerate(row):
                self.__blocks.append(self.__canvas.create_image(
                    (16 * (j - delta_x) + 8) * ZOOM,
                    (16 * (i - delta_y) + 8) * ZOOM,
                    image=self.__ow_sprites[tile.get_type()])
                )
        self.__trainer = self.__canvas.create_image(
            (16 * (self.__x - delta_x ) + 8) * ZOOM,
            (16 * (self.__y - delta_y) + 8) * ZOOM,
            image=self.__ow_sprites["down"]
        )

    def ticker(self):
        self.up()
        self.__mw.after(10, self.ticker)

    def up(self):
        self.__num += 0.01
        self.__numlbl["text"] = "{:.2f}".format(self.__num)

    def down(self):
        self.__num -= 1
        self.__numlbl["text"] = str(self.__num)

    def movement_animation(self, x, y, direction):
        self.__ongoing_animation = True
        walkstring = "walk_" + direction
        for block in self.__blocks:
            self.__canvas.move(block, 4 * x * ZOOM, 4 * y * ZOOM)
        self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites[walkstring])
        self.__mw.update()
        sleep(0.05)
        for block in self.__blocks:
            self.__canvas.move(block, 4 * x * ZOOM, 4 * y * ZOOM)
        self.__mw.update()
        sleep(0.05)
        for block in self.__blocks:
            self.__canvas.move(block, 4 * x * ZOOM, 4 * y * ZOOM)
        self.__mw.update()
        sleep(0.05)
        for block in self.__blocks:
            self.__canvas.move(block, 4 * x * ZOOM, 4 * y * ZOOM)
        self.__canvas.itemconfig(self.__trainer, image=self.__ow_sprites[direction])
        self.__mw.update()
        self.__ongoing_animation = False


#def main():
#    GUI()


#main()