__author__ = 'Emilio'
import tkinter as tk
import myconstants as m_c
from player_obj import pd
from pointbar import PointBar
from bar_button import BarButton
from info_bar import InfoBar
from player_ailments_bar import PlayerAilmentsBar

import playerData as pd

hp_bar = None
mp_bar = None
playerFX = None
buttons = [[None for i in range(4)] for j in range(2)]

class StatBar:
    def __init__(self, master, my_time, my_msg, player):
        self.master = master
        self.my_msg = my_msg
        self.my_time = my_time
        self.my_player = player

        self.make_hpmp_bars()
        self.make_spacers()
        self.make_mid_buttons()

        hover_frame = tk.Frame(master, bg="green", width=m_c.hover_w, height=m_c.hover_h, highlightthickness=0)
        hover_frame.grid(row=1, column=7, rowspan=2)

        self.hover_bar = InfoBar(hover_frame, my_time)
        self.playerFX = PlayerAilmentsBar(master, my_time, player)
        self.playerFX.attach_message_core(self.my_msg)
        self.playerFX.register_object()

    def make_mid_buttons(self):
        button_canvas = [[None for j in range(4)] for i in range(2)]
        for i in range(2):
            for j in range(4):
                button_canvas[i][j] = tk.Canvas(self.master, bg='gray', width=m_c.button_w, height=m_c.button_h,
                                                highlightthickness=0)
                buttons[i][j] = BarButton("errorBlock", self.my_time)
                buttons[i][j].attach_canvas(button_canvas[i][j])
                button_canvas[i][j].grid(row=1 + i, column=2 + j)

        # populate elementary moves
        for x in range(4):
            buttons[0][x].replace_image(pd.MOVELIST[x][1])
            buttons[0][x].register_object()
            buttons[0][x].register_move(self.my_player, x)
            buttons[0][x].attach_message_core(self.my_msg)
            buttons[0][x].add_button_description(pd.MOVELIST[x][2], pd.MOVELIST[x][3])
            self.my_player.bind_button(buttons[0][x], pd.MOVELIST[x][1])
        # throw is also an elementary move that toggles from Grab
        self.my_player.bind_button(buttons[0][pd.GRAB], pd.MOVELIST[pd.THROW][1])

    def make_spacers(self):
        self.fill_wall = tk.PhotoImage(file="./images/statbar/filler.gif")
        fill_canvas1 = tk.Canvas(self.master, bg="blue", width=m_c.button_w, height=m_c.button_h * 2,
                                 highlightthickness=0)
        fill_canvas1.grid(row=1, column=1, rowspan=2)
        fill_canvas1.create_image(0, 0, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas1.create_image(0, 50, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas2 = tk.Canvas(self.master, bg="blue", width=m_c.button_w, height=m_c.button_h * 2,
                                 highlightthickness=0)
        fill_canvas2.grid(row=1, column=6, rowspan=2)
        fill_canvas2.create_image(0, 0, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas2.create_image(0, 50, anchor=m_c.anchor, image=self.fill_wall)

    def make_hpmp_bars(self):
        # HP Bar
        global hp_bar, mp_bar
        hp_bar = PointBar("playerHP", self.my_time)
        hpcanvas = tk.Canvas(self.master, bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        hp_bar.attach_canvas(hpcanvas)
        hp_bar.create_bar_image()
        hpcanvas.grid(row=1, column=0)
        hp_bar.register_object()
        # MP Bar
        mpcanvas = tk.Canvas(self.master, bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        mp_bar = PointBar("playerMP", self.my_time)
        mp_bar.attach_canvas(mpcanvas)
        mp_bar.create_bar_image()
        mpcanvas.grid(row=2, column=0)
        mp_bar.recolor_bar("light blue", "blue")
        mp_bar.retype_bar("MP")
        mp_bar.register_object()

        player = self.my_player
        player.attach_hp_mp_bar(hp_bar,mp_bar)

    def get_hover(self):
        return self.hover_bar
