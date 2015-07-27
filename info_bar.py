import tkinter as tk
from animatable import ProtoAnim
from pointbar import PointBar
import myconstants as m_c
msg_hp = None #they need to be up here to prevent stupid garbage collection
msg_mp = None
text_cover = None

class InfoBar(ProtoAnim):
    TEXT = 0
    HPMP = 1
    def __init__(self, info_frame, my_time):
        self.info_frame = info_frame
        ProtoAnim.__init__(self,"info box",my_time)
        self.active_canvas = 0
        self.attach_canvas()

        self.tick_til = 20

        self.populate_hpmp_canvas()
        self.populate_text_canvas()
        self.activate_canvas(InfoBar.TEXT)
        #self.register_object()

    def populate_text_canvas(self):
        global text_cover
        text_cover = tk.PhotoImage(file = './images/statbar/hovercover.gif')

        self.my_canvas[InfoBar.TEXT].create_text(15,12, anchor="nw",text="asdf",tag="bigtext",font="helvetica 12 bold", width = 120)
        self.my_canvas[InfoBar.TEXT].create_text(15,30, anchor="nw",text="asdf",tag="smalltext",font="helvetica 9 italic", width = 120)

        self.my_canvas[InfoBar.TEXT].create_image(0,0, anchor="nw",image=text_cover,tag="cover")

    def rewrite_text(self,val1,val2):
        self.my_canvas[InfoBar.TEXT].itemconfig("bigtext",text=val1)
        self.my_canvas[InfoBar.TEXT].itemconfig("smalltext",text=val2)

    def populate_hpmp_canvas(self):
        global msg_hp, msg_mp
        msg_hp = PointBar("msgHP", self.my_time)
        msg_mp = PointBar("msgMP", self.my_time)
        hpcanvas = tk.Canvas(self.my_canvas[InfoBar.HPMP], bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        msg_hp.attach_canvas(hpcanvas)
        msg_hp.create_bar_image()
        hpcanvas.grid(row=0, column=0)
        # MP Bar
        mpcanvas = tk.Canvas(self.my_canvas[InfoBar.HPMP], bg='pink', width=m_c.bar_w, height=m_c.bar_h, highlightthickness=0)
        msg_mp.attach_canvas(mpcanvas)
        msg_mp.create_bar_image()
        mpcanvas.grid(row=1, column=0)
        msg_mp.recolor_bar("light blue", "blue")
        msg_mp.retype_bar("MP")

    def attach_canvas(self,canvas=None):
        self.my_canvas = [None for x in range(2)]

        self.my_canvas[InfoBar.TEXT] = tk.Canvas(self.info_frame,bg = 'light gray', width=m_c.hover_w, height=m_c.hover_h,highlightthickness=0)
        self.my_canvas[InfoBar.HPMP] = tk.Canvas(self.info_frame,bg = 'green', width=m_c.hover_w, height=m_c.hover_h,highlightthickness=0)
        for c in self.my_canvas:
            c.grid(row=0,column=0,sticky='NESW')

    def activate_canvas(self,num):
        self.active_canvas = num
        #need a special tkinter lift for canvases. go figure.
        tk.Misc.lift(self.my_canvas[num])


    def animate_tick(self):
        self.tick +=1
        if self.tick >= self.tick_til:
            self.animate()

    def animate(self):
        self.activate_canvas((self.active_canvas + 1)%2)
        self.tick = 0


