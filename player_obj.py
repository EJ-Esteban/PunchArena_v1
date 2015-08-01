import tkinter as tk
import myconstants as m_c
from animatable import ProtoAnim

import playerData as pd


# player object containing data relevant to both computer and human players

class Player(ProtoAnim):
    CONSOLE_DETAIL = m_c.PLAYER_CONSOLE_DETAIL
    key_map = {'q': pd.WALK, 'w': pd.PUNCH,
               'e': pd.BLOCK, 'r': pd.GRAB}

    def __init__(self, name, my_time, NPC=True):
        ProtoAnim.__init__(self, name, my_time)

        self.tick_til = pd.PLAYER_ANIM_DELAY
        self.facing = m_c.NORTH

        self.mode = pd.WALK

        self.x = self.y = 0
        self.next_x = self.next_y = 0

        self.active_effects = []

        if not NPC:
            self.buttons = dict()

    def attach_canvas(self, canvas=None):
        # players should attach to world canvas
        self.my_canvas = canvas

    def attach_worldmap(self, map_obj):
        self.my_world = map_obj

    def bind_button(self, obj, key):
        self.buttons[key] = obj

    def unbind_button(self, key):
        if key in self.buttons.keys():
            del self.buttons[key]

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        self.send_to_console("moving player \"" + self.name + "\"", "x: " + str(self.x) + "\ty: " + str(self.y), val=4)
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
        self.send_to_console("loading player sprites....", val=2)
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

    def add_effect(self, value):
        if not self.has_effect(value) and value in pd.VALID_EFFECTS.keys():
            self.active_effects.append(value)

    def has_effect(self, value):
        return value in self.active_effects

    def rm_effect(self, value):
        if self.has_effect(value):
            self.active_effects.remove(value)

    def rm_foot_effects(self):
        for effect in pd.FOOT_EFFECTS:
            self.rm_effect(effect)

    def rm_hand_effects(self):
        for effect in pd.HAND_EFFECTS:
            self.rm_effect(effect)

    def add_hand_effect(self, variant):
        self.rm_hand_effects()
        self.add_effect(variant)

    def cycle_move(self):
        self.mode += 1
        self.mode %= pd.HIGH_MOVE + 1
        move = pd.MOVELIST[self.mode]
        self.send_to_console("Equipped move " + move[0], val=3)

    def set_move(self, num):
        self.mode = num
        move = pd.MOVELIST[self.mode]
        self.send_to_console("Equipped move " + move[0], val=3)

    def is_turn(self):
        return self.game_state.player_can_move(1)

    def move_arrow(self, dir):
        self.rm_effect("blocking")
        if self.mode in [pd.WALK, pd.BLOCK, pd.PUNCH]:
            getattr(self, pd.MOVELIST[self.mode][0])(dir)

    def spacebar(self):
        self.rm_effect("blocking")
        if self.mode in [pd.GRAB, pd.THROW]:
            getattr(self, pd.MOVELIST[self.mode][0])()

    def grab(self, dir=-1):
        if dir == -1:
            self.my_world.service_tile(self.x, self.y, self)

        button = self.buttons[pd.MOVELIST[pd.GRAB][1]]
        button.replace_image(pd.MOVELIST[pd.THROW][1])
        button.register_move(self, pd.THROW)
        button.add_button_description(pd.MOVELIST[pd.THROW][2], pd.MOVELIST[pd.THROW][3])
        self.mode = pd.THROW
        self.key_map['r'] = pd.THROW

    def throw(self, dir=-1):
        print("throw")
        if dir == -1:
            self.rm_hand_effects()
            self.my_world.service_tile(self.x, self.y, self)

        button = self.buttons[pd.MOVELIST[pd.THROW][1]]
        button.replace_image(pd.MOVELIST[pd.GRAB][1])
        button.register_move(self, pd.GRAB)
        button.add_button_description(pd.MOVELIST[pd.GRAB][2], pd.MOVELIST[pd.GRAB][3])
        self.mode = pd.GRAB
        self.key_map['r'] = pd.GRAB

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
        s = "punching tile at " + str(self.next_x) + "," + str(self.next_y)
        if punched:
            s += "\nBroke a tile!"
        self.send_to_console(s, val=2)
        self.my_world.service_tile(self.next_x, self.next_y, self)
        self.anim_frame = 2  # set to punch frame
        self.tick_til = pd.PLAYER_ANIM_DELAY_LONG
        self.animate()

    def block(self, dir):
        self.facing = dir
        self.add_effect("blocking")
        self.animate()

    def walk(self, dir):
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
        s = "Path was "
        if self.my_world.can_walk_tile(self.next_x, self.next_y):
            self.set_coords(self.next_x, self.next_y)
            s += "taken."
        else:
            s += "blocked."
        s += "\n"
        self.send_to_console(
            "Trying to move Player " + self.name + " to " + str(self.next_x) + "," + str(self.next_y), s, val=2)
        self.my_world.service_tile(self.x, self.y, self)
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
