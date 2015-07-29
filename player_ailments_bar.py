import tkinter as tk
from animatable import ProtoAnim
import myconstants as m_c
import playerData as pd


class PlayerAilmentsBar(ProtoAnim):
    def __init__(self, master, time_core, player):
        self.master = master
        ProtoAnim.__init__(self, "PlayerFX", time_core)
        self.attach_canvas()
        self.cover = tk.PhotoImage(file="./images/statbar/FXCover.gif")
        self.my_canvas.create_image(0, 0, anchor=m_c.anchor, image=self.cover, tag="cover")
        self.player = player

        self.effect_count = 0
        self.effect_list = []

    def attach_canvas(self):
        self.my_canvas = tk.Canvas(self.master, bg="light gray", width=m_c.canvas_w, height=m_c.button_h,
                                   highlightthickness=0)
        self.my_canvas.grid(row=0, column=0, columnspan=8)

    def add_box(self, effect):
        if effect in self.effect_list:
            return
        self.effect_list.append(effect)
        self.effect_count += 1
        self.my_canvas.create_rectangle(0, 0, 0, 0, fill="red", tag=effect, width=1)
        self.my_canvas.tag_bind(effect, "<Enter>", lambda event, foo=effect: self.hover_in(foo))
        self.my_canvas.tag_bind(effect, "<Leave>", self.hover_out)

    def rm_box(self, effect):
        if effect not in self.effect_list:
            return
        self.effect_list.remove(effect)
        self.effect_count -= 1
        self.msg_pipe.remove_message_candidate(self.msg_tag)
        self.my_canvas.delete(effect)

    def redraw(self):
        ymin = 15
        ymax = 34
        i = 0
        for effect in self.effect_list:
            xmin = 166 + 26 * i
            xmax = 185 + 26 * i
            self.my_canvas.coords(effect, xmin, ymin, xmax, ymax)
            self.my_canvas.itemconfig(effect, fill=pd.VALID_EFFECTS[effect][2])
            i += 1

    def animate_tick(self):
        to_add = []
        to_rm = []

        for effect in self.player.active_effects:
            if effect not in self.effect_list:
                to_add.append(effect)
        for effect in self.effect_list:
            if effect not in self.player.active_effects:
                to_rm.append(effect)

        for effect in to_add:
            self.add_box(effect)
        for effect in to_rm:
            self.rm_box(effect)
        if not to_add == [] or not to_rm == []:
            self.redraw()

    def bind_listeners(self):
        self.msg_tag = self.name
        # no listeners--adding thing will

    def hover_in(self, effect):
        self.mousedover = True
        bigtext = pd.VALID_EFFECTS[effect][0]
        littletext = pd.VALID_EFFECTS[effect][1]
        self.msg_packet = ['hover', bigtext, littletext, m_c.PRIO_HOVER_BACK, 0, False]
        self.msg_pipe.add_message_candidate(self.msg_tag, self.msg_packet)

    def hover_out(self, event):
        self.mousedover = False
        self.msg_pipe.remove_message_candidate(self.msg_tag)
