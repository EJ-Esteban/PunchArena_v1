"""
pointbar.py
hp and mp bars and crap
"""

import tkinter as tk
import myconstants as m_c
from animatable import ProtoAnim

BAR_LOW = 10
BAR_HI = 101


class PointBar(ProtoAnim):
    def __init__(self, name, my_time):
        ProtoAnim.__init__(self, name, my_time)
        self.max_val = 10
        self.cur_val = 10

    def attach_canvas(self, canvas=None):
        self.my_canvas = canvas

    def create_bar_image(self):
        self.sprite = tk.PhotoImage(file='./images/statbar/barcover.gif')
        self.my_canvas.create_rectangle(BAR_LOW, 0, BAR_HI, 50, fill="red", tag="bar", width=0)
        self.my_canvas.create_image(0, 0, anchor=m_c.anchor, image=self.sprite, tag="cover")
        self.my_canvas.create_text(105, 8, font=m_c.barfonts, anchor=tk.NW, text=str(self.cur_val) + "/", tag="curtext",
                                   width="40")
        self.my_canvas.create_text(105, 22, font=m_c.barfonts, anchor=tk.NW, text=str(self.max_val), tag="maxtext",
                                   width="40")
        self.my_canvas.create_text(40, 10, font=m_c.barnamefont, anchor=tk.NW, text="HP", tag="nametext", width="40")

    def recolor_bar(self, canv_color, bar_color):
        """recolor bar, ex. to make mana colored"""
        self.my_canvas.config(bg=canv_color)
        self.my_canvas.itemconfig("bar", fill=bar_color)
        self.my_canvas.update()

    def retype_bar(self, txt, fill="black"):
        """change bar text"""
        self.my_canvas.itemconfig("nametext", fill=fill, text=txt)

    def update_bar_nums(self):
        self.my_canvas.itemconfig("curtext", text=str(self.cur_val) + "/")
        self.my_canvas.itemconfig("maxtext", text=str(self.max_val))

    def update_bar(self):
        self.update_bar_nums()
        pctFull = float(self.cur_val / self.max_val)
        if (pctFull < 0):
            pctFull = 0
        if (pctFull > 1):
            pctFull = 1
        barcoord = BAR_LOW + int((BAR_HI - BAR_LOW) * pctFull)
        self.my_canvas.coords("bar", BAR_LOW, 0, barcoord, 50)

    def lose_point(self, amt):
        self.cur_val -= amt
        if self.cur_val < 0:
            self.cur_val = 0
        self.update_bar()
