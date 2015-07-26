__author__ = 'Emilio'
import tkinter as tk
import myconstants as m_c
from player_obj import Player
from world_obj import World_map
from pointbar import PointBar
from bar_button import BarButton

hp_bar = PointBar()
mp_bar = PointBar()
buttons = [[None for i in range(4)] for j in range(2)]
hover_frame = None

class StatBar:
    def __init__(self, master, my_time, player):
        self.master = master
        self.my_time = my_time
        self.my_player = player

        self.make_hpmp_bars()
        self.make_spacers()
        self.make_mid_buttons()

        hover_frame = tk.Frame(master,bg="green",width=m_c.hover_w,height=m_c.hover_h,highlightthickness=0)
        hover_frame.grid(row=0,column=7,rowspan=2)

    def make_mid_buttons(self):
        button_canvas = [[None for j in range(4)] for i in range(2)]
        for i in range(2):
            for j in range(4):
                button_canvas[i][j] = tk.Canvas(self.master, bg='gray', width=m_c.button_w, height=m_c.button_h,
                                                highlightthickness=0)
                buttons[i][j] = BarButton("errorBlock",self.my_time)
                buttons[i][j].attach_canvas(button_canvas[i][j])
                button_canvas[i][j].grid(row=i, column=2 + j)
        #special buttons
        buttons[0][0].replace_image("moveButton")
        buttons[0][0].register_object()
        buttons[0][0].register_move(self.my_player,Player.WALK)
        buttons[0][1].replace_image("blockButton")
        buttons[0][1].register_object()
        buttons[0][1].register_move(self.my_player,Player.BLOCK)
        buttons[0][2].replace_image("punchButton")
        buttons[0][2].register_object()
        buttons[0][2].register_move(self.my_player,Player.PUNCH)

    def make_spacers(self):
        self.fill_wall = tk.PhotoImage(file="./images/statbar/filler.gif")
        fill_canvas1 = tk.Canvas(self.master, bg="blue", width=m_c.button_w, height=m_c.button_h * 2, highlightthickness=0)
        fill_canvas1.grid(row=0, column=1, rowspan=2)
        fill_canvas1.create_image(0, 0, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas1.create_image(0, 50, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas2 = tk.Canvas(self.master, bg="blue", width=m_c.button_w, height=m_c.button_h * 2, highlightthickness=0)
        fill_canvas2.grid(row=0, column=6, rowspan=2)
        fill_canvas2.create_image(0, 0, anchor=m_c.anchor, image=self.fill_wall)
        fill_canvas2.create_image(0, 50, anchor=m_c.anchor, image=self.fill_wall)

    def make_hpmp_bars(self):
        #HP Bar
        hpcanvas = tk.Canvas(self.master, bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        hp_bar.attach_canvas(hpcanvas)
        hp_bar.create_bar_image()
        hpcanvas.grid(row=0, column=0)
        #MP Bar
        mpcanvas = tk.Canvas(self.master, bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        mp_bar.attach_canvas(mpcanvas)
        mp_bar.create_bar_image()
        mpcanvas.grid(row=1, column=0)
        mp_bar.recolor_bar("light blue", "blue")
        mp_bar.retype_bar("MP")

    def animate(self,player):
        if(player.action=="walk"):
            buttons[0][0].replace_cover(True)
            buttons[0][2].replace_cover(False)
        elif(player.action=="punch"):
            buttons[0][2].replace_cover(True)
            buttons[0][0].replace_cover(False)

