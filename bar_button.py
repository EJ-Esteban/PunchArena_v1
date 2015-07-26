__author__ = 'Emilio'

import tkinter as tk
import myconstants as m_c
from animatable import ProtoAnim

class BarButton(ProtoAnim):
    def __init__(self, name, time_core):
        ProtoAnim.__init__(self,name,time_core)
        self.mode = -1


    def attach_canvas(self,canvas):
        self.my_canvas=canvas
        self.place_images()

    def place_images(self):
        self.button_img = tk.PhotoImage(file="./images/statbar/"+self.name + ".gif")
        self.cover_img = tk.PhotoImage(file="./images/statbar/buttonCover.gif")
        self.cover_img2 = tk.PhotoImage(file="./images/statbar/buttonCover_hilit.gif")
        self.my_canvas.create_image(0, 0, anchor=m_c.anchor, image=self.button_img, tag = "button")
        self.my_canvas.create_image(0, 0, anchor=m_c.anchor, image=self.cover_img, tag = "cover")

    def replace_cover(self,status):
        #true = light tile
        if status:
            self.my_canvas.itemconfig("cover",image=self.cover_img2)
        else:
            self.my_canvas.itemconfig("cover",image=self.cover_img)
        self.my_canvas.update()

    def replace_image(self,imgname):
        self.name = imgname
        self.button_img = tk.PhotoImage(file="./images/statbar/" + self.name +".gif")
        self.my_canvas.itemconfig("button",image=self.button_img)

    def register_move(self,player,number):
        self.player = player
        self.mode = number

    def animate_tick(self):
        self.replace_cover(self.player.check_mode()==self.mode)

