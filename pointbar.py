"""
pointbar.py
hp and mp bars and crap
"""

import tkinter as tk
import myconstants as m_c
import math
from animatable import ProtoAnim


class PointBar(ProtoAnim):
    BAR_LOW = 10
    BAR_HI = 101
    play_states = ['static', 'drain', 'flash']

    def __init__(self, name, my_time):
        ProtoAnim.__init__(self, name, my_time)
        # values (10 by default)
        self.max_val = 10
        self.cur_val = 10
        self.pctfull = 1.0
        # animation overhead references (only really in use if animation is playing
        self.player = None
        self.play_state = 'static'
        self.dx = 0.0
        self.anim_count = 0
        self.block = False
        self.rounding_insurance = 0
        self.flashcount = 2

    def attach_canvas(self, canvas=None):
        self.my_canvas = canvas

    def create_bar_image(self):
        self.sprite = tk.PhotoImage(file='./images/statbar/barcover.gif')
        self.my_canvas.create_rectangle(PointBar.BAR_LOW, 0, PointBar.BAR_HI, 50, fill="white", tag="flash", width=0)
        self.my_canvas.create_rectangle(PointBar.BAR_LOW, 0, PointBar.BAR_HI, 50, fill="red", tag="bar", width=0)
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

    def fast_redraw(self, new_cur=None, new_max=None):
        if new_cur is not None or new_max is not None:
            self.cur_val = new_cur
            self.max_val = new_max
        self.update_bar_nums()
        self.pctFull = float(self.cur_val / self.max_val)
        if (self.pctFull < 0):
            self.pctFull = 0.0
        if (self.pctFull > 1):
            self.pctFull = 1.0
        barcoord = PointBar.BAR_LOW + int((PointBar.BAR_HI - PointBar.BAR_LOW) * self.pctFull)
        self.my_canvas.coords("flash", PointBar.BAR_LOW, 0, barcoord, 50)
        self.my_canvas.coords("bar", PointBar.BAR_LOW, 0, barcoord, 50)

    def fast_lose_point(self, amt):
        # fast draining of bar
        self.cur_val -= amt
        if self.cur_val < 0:
            self.cur_val = 0
        self.fast_redraw()

    def start_drain_points(self, player, amount, type='hp', blocking = True):
        self.player = player
        self.cur_val = player.check_stat(type)
        self.max_val = player.check_stat('max_' + type)
        if (self.cur_val - amount) < 0:
            amount = self.cur_val
        # store the proper amount lost to ensure that no rounding errors occur
        # set current to rounding insurance after process is over
        self.rounding_insurance = self.cur_val - amount
        # max drain time is 15 ticks (750 ms)--if you lose almost all your points at once
        self.anim_count = int(14 * math.sqrt(amount / self.max_val)) + 1
        self.dx = float(amount/(self.anim_count * self.max_val))
        # completely redraw with thesse new numbers to start animation
        #this also resets percent full
        self.fast_redraw()
        self.play_state = 'drain'
        self.flashcount = 4
        if blocking:
            self.block = True
            self.my_time.add_blocking_animation()

    def animate_tick(self):
        if self.play_state == 'static':
            return
        elif self.play_state == 'drain':
            self.pctFull = self.pctFull - self.dx
            if (self.pctFull < 0):
                self.pctFull = 0.0
            barcoord = PointBar.BAR_LOW + int((PointBar.BAR_HI - PointBar.BAR_LOW) * self.pctFull)
            self.cur_val = int(self.pctFull * self.max_val)
            self.my_canvas.coords("bar", PointBar.BAR_LOW, 0, barcoord, 50)
            self.update_bar_nums()
            self.anim_count-= 1
            if self.anim_count <= 0:
                #really should never be less than 0 but here we are
                self.anim_count = 3
                self.play_state = 'flash'
        elif self.play_state == 'flash':
            self.anim_count-= 1
            if self.anim_count <= 0:
                self.flashcount -=1
                if (self.flashcount %2) == 0:
                    self.my_canvas.itemconfig("flash", state = "normal")
                else:
                    self.my_canvas.itemconfig("flash", state = "hidden")
                self.anim_count = 3
                if self.flashcount <= 0:
                    barcoord = PointBar.BAR_LOW + int((PointBar.BAR_HI - PointBar.BAR_LOW) * self.pctFull)
                    self.my_canvas.coords("flash", PointBar.BAR_LOW, 0, barcoord, 50)
                    if self.block:
                        self.my_time.rm_blocking_animation()
                        self.block = False
                    self.player.cur_value = self.rounding_insurance
                    self.update_bar_nums()
                    self.player.hp = self.rounding_insurance
                    self.play_state = 'static'
        else:
            self.send_to_console("A pointbar was found in an invalid animation state.", val=1)
            self.play_state == 'static'
