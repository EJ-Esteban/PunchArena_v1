import tkinter as tk
import myconstants as m_c
from animatable import ProtoAnim

import playerData as pd

# player object containing data relevant to both computer and human players

class Player(ProtoAnim):

    def __init__(self, name, my_time):
        ProtoAnim.__init__(self, name, my_time)

        self.tick_til = pd.PLAYER_ANIM_DELAY
        self.facing = m_c.NORTH

        self.mode = pd.WALK

        self.x = self.y = 0
        self.next_x = self.next_y = 0


    def attach_canvas(self, canvas=None):
        # players should attach to world canvas
        self.my_canvas = canvas

    def attach_worldmap(self, map_obj):
        self.my_world = map_obj

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        if self.console_ready(4):
            self.send_to_console("moving player \"" + self.name + "\"","x: " + str(self.x) +"\ty: " + str(self.y))
        self.my_canvas.coords(self.name, self.x * 50, self.y * 50)
        self.my_canvas.update()

    def check_mode(self):
        return self.mode

    def create_sprite(self, name):
        self.load_tiles()
        self.name = name
        self.my_canvas.create_image(0, 0, anchor="nw", image=self.animArray[0][0], tag=name)

    def load_tiles(self):
        """loads images into animation array"""
        if self.console_ready(2):
            self.send_to_console("loading player sprites....")
        self.animArray = [[None for i in range(3)] for j in range(4)]
        # "bob" (generic protagonist) sprites
        for c in range(3):
            self.animArray[m_c.NORTH][c] = tk.PhotoImage(file=m_c.sprite_image("bobN" + str(c)))
            self.animArray[m_c.EAST][c] = tk.PhotoImage(file=m_c.sprite_image("bobE" + str(c)))
            self.animArray[m_c.SOUTH][c] = tk.PhotoImage(file=m_c.sprite_image("bobS" + str(c)))
            self.animArray[m_c.WEST][c] = tk.PhotoImage(file=m_c.sprite_image("bobW" + str(c)))

    def animate_tick(self):
        """forces animate on tick"""
        self.tick += 1
        if self.tick >= self.tick_til:
            self.animate()

    def cycle_move(self):
        self.mode += 1
        self.mode %= pd.HIGH_MOVE + 1
        if self.console_ready(2):
            move = pd.MOVELIST[self.mode]
            self.send_to_console("Queued move " + move[0])

    def set_move(self, num):
        self.mode = num
        if self.console_ready(2):
            move = pd.MOVELIST[self.mode]
            self.send_to_console("Queued move " + move[0])

    def is_turn(self):
        return self.game_state.player_can_move(1)

    def move_arrow(self, dir):
        if self.mode == pd.PUNCH:
            self.punch(dir)
        elif self.mode == pd.BLOCK:
            pass
        else:  # walk mode
            self.move(dir)

    def punch(self, dir):
        self.facing = dir
        dx = 0
        dy = 0
        if dir == m_c.NORTH:
            dy = -1
        elif dir == m_c.EAST:
            dx = 1
        elif dir == m_c.WEST:
            dx = -1
        else:
            dy = 1
        self.predict(dx, dy)
        punched = self.my_world.can_break_tile(self.next_x, self.next_y)
        if punched:
            self.my_world.degrade_tile(self.next_x, self.next_y)
        if self.console_ready(2):
            s = ""
            if punched:
                s = "Broke a tile!"
            self.send_to_console("punching tile at " + str(self.next_x) + "," + str(self.next_y), s)
        self.anim_frame = 2  # set to punch frame
        self.tick_til = pd.PLAYER_ANIM_DELAY_LONG
        self.animate()

    def move(self, dir):
        if not self.is_turn():
            return
        self.facing = dir
        dx = 0
        dy = 0
        if dir == m_c.NORTH:
            dy = -1
        elif dir == m_c.EAST:
            dx = 1
        elif dir == m_c.WEST:
            dx = -1
        else:
            dy = 1
        self.predict(dx, dy)
        col = self.my_world.can_walk_tile(self.next_x, self.next_y)
        if col:
            self.set_coords(self.next_x, self.next_y)
            spc = self.my_world.tile_is_special(self.x, self.y)
        if self.console_ready(2):
            s = "Path was "
            if not col:
                s += "blocked."
            else:
                s += "taken."
                if not spc == "":
                    s += "\n" + self.name + " walked onto special tile: " + spc
            self.send_to_console("Trying to move to " + str(self.next_x) + "," + str(self.next_y), s)

        self.animate()

    def predict(self, dx, dy):
        # adds coordinates to try
        self.next_x = self.x + dx
        self.next_y = self.y + dy
        # prepares to wrap around if nothing else
        if (self.next_x < 0):
            self.next_x = 11
        if (self.next_x > 11):
            self.next_x = 0
        if (self.next_y < 0):
            self.next_y = 7
        if (self.next_y > 7):
            self.next_y = 0

    def console_ready(self, val):
        return m_c.MASTER_CONSOLE and val <= m_c.PLAYER_CONSOLE_DETAIL

    def animate(self):
        """take action on animatino"""
        self.my_canvas.itemconfig(self.name, image=self.animArray[self.facing][self.anim_frame])
        self.anim_frame += 1  # advance frame
        self.anim_frame %= 2  # basic walk cycle is the first 2 things, and we always go back to basic walk cycle
        self.my_canvas.update()
        self.tick = 0
        if self.console_ready(5):
            self.send_to_console("animating player")

    def bind_listeners(self):
        self.msg_tag = self.name
        self.my_canvas.tag_bind(self.name, "<Enter>", self.hover_in)
        self.my_canvas.tag_bind(self.name, "<Leave>", self.hover_out)

    def hover_in(self, event):
        self.msg_packet = ['hover', 'player', 'hey that\'s you!', m_c.PRIO_HOVER_FORE, -1, False]
        self.msg_pipe.add_message_candidate(self.msg_tag, self.msg_packet)

    def hover_out(self, event):
        self.msg_pipe.remove_message_candidate(self.msg_tag)
