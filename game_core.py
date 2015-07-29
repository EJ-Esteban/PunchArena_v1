__author__ = 'Emilio'

import tkinter as tk
import myconstants as m_c
from player_obj import Player
from world_obj import World_map

from lower_bar import StatBar

from threading import Semaphore

game_object = None
game_console = None

class Game:
    def __init__(self, master):
        global game_object
        game_object = self
        self.launch_game_cores(master)
        self.launch_game_graphics(master,'tt')
        self.launch_game_listeners(master)
        self.my_time.start_game_ticks()

    def launch_game_cores(self, master):
        # create state machine core
        self.my_state = StateCore()
        # create message core
        self.my_msg = MessageCore(self.my_state)
        # create time core (animation, state machine update)
        self.my_time = TimeCore(master, self.my_state, self.my_msg)

    def launch_game_graphics(self, master,arena ='tt'):
        # setup window
        self.master = master
        master.wm_title("Punch Arena v." + m_c.VERSION_NUMBER)
        # setup canvases
        map_canvas = tk.Canvas(master, bg='pink', width=m_c.canvas_w, height=m_c.canvas_h1, highlightthickness=0)
        map_canvas.pack()
        self.game_arena = World_map(self.my_time, self.my_msg, map_canvas, arena)
        self.place_player_char(map_canvas)
        statbar_frame = tk.Frame(master, bg='red', width=m_c.canvas_w, height=m_c.canvas_h2, highlightthickness=0)
        statbar_frame.pack()
        self.statbar = StatBar(statbar_frame, self.my_time, self.my_msg, self.player1)
        self.hover_box = self.statbar.get_hover()
        self.my_msg.register_hoverbox(self.hover_box)

    def place_player_char(self, map_canvas):
        # create player
        self.player1 = Player("player1", self.my_time)
        # associate player with canvas, create sprite, and register for animation
        self.player1.attach_canvas(map_canvas)
        self.player1.create_sprite("player1")
        self.player1.register_object()
        # this object DOES need access to the game state machine
        self.player1.attach_state_machine(self.my_state)
        self.player1.attach_worldmap(self.game_arena)
        self.player1.attach_message_core(self.my_msg)
        self.player1.set_coords(self.game_arena.playerPos[0], self.game_arena.playerPos[1])

    def launch_game_listeners(self, master):
        # bind listeners
        master.bind("<space>", GameInput.space_detect)
        master.bind('<Left>', GameInput.leftKey)
        master.bind('<Right>', GameInput.rightKey)
        master.bind('<Up>', GameInput.upKey)
        master.bind('<Down>', GameInput.downKey)
        master.bind('<KeyPress>', GameInput.key_detect)

    def attach_console(self,console):
        global game_console
        game_console = console


class TimeCore:
    def __init__(self, tkinter_master, state_core, msg_core, tick_mod=10000):
        self.master = tkinter_master
        self.state_core = state_core
        self.msg_core = msg_core
        # initialize blank list of animation objects
        self.anim_objects = []
        # tick_mod is a constant number for "clocking" events
        self.tick_num = 0
        self.tick_mod = tick_mod  # 10k by default
        # blocking animation semaphore and count
        self.blocking_anims = 0
        self.blocking_sem = Semaphore()

    def add_anim_actor(self, anim_actor):
        # register actor onto object animation list
        if anim_actor not in self.anim_objects:
            self.anim_objects.append(anim_actor)

    def del_anim_actor(self, anim_actor):
        # remove actor object from animation list
        if anim_actor in self.anim_objects:
            self.anim_objects.remove(anim_actor)

    def start_game_ticks(self):
        self.master.after(m_c.ANIM_START_DELAY, self.tick)
        self.state_core.finish_setup()

    def tick(self):
        for o in self.anim_objects:
            o.animate_tick();
        self.msg_core.play_messages()
        self.master.after(m_c.ANIM_DT, self.tick)

    def animation_blocked(self):
        probe = True
        self.blocking_sem.acquire()
        probe = (self.blocking_anims > 0)
        self.blocking_sem.release()
        return probe


class StateCore:
    valid_states = ('setup', 'player_turn', 'in_turn_wait',
                    'pre_turn_wait', 'change_players', 'endgame', 'error')

    def __init__(self):
        self.state = 'setup'
        self.player = 1

    def check_state(self):
        if self.state not in StateCore.valid_states:
            self.state = 'error'
        return self.state

    def player_can_move(self, num):
        # creates concept of "turns
        return (self.state == 'player_turn') & (self.player == num)

    def finish_setup(self):
        self.state = 'player_turn'

    def win_game(self):
        self.state = 'endgame'


class MessageCore:
    def __init__(self, state):
        self.venues = ['console']
        self.tag_list = []
        self.my_state = state
        self.messages = dict()

    def register_hoverbox(self, box):
        self.hover_box = box
        self.venues.append('hover')

    def add_message_candidate(self, tag, packet):
        self.tag_list.append(tag)
        self.messages[tag] = packet

    def remove_message_candidate(self, tag):
        if tag in self.tag_list:
            self.tag_list.remove(tag)
        if tag in self.messages.keys():
            del self.messages[tag]

    def elect_messages(self):
        winners = dict()
        winningtag = dict()
        for venue in self.venues:
            winners[venue] = [venue, '', '', -1, 0, False]  # blank packet
            for tag in self.messages.keys():
                if self.messages[tag][0] == venue:
                    try_packet = self.messages[tag]
                    if try_packet[3] > winners[venue][3]:
                        winners[venue] = self.messages[tag]
                        winningtag[venue] = tag
        return winners,winningtag

    def play_messages(self):
        messages,tags = self.elect_messages()

        # plays leading console message
        if not (messages['console'][3] == -1):  # eliminates blank messages
            consoletext = messages['console'][1]
            consoletext += "\n" + messages['console'][2]
            if game_console: #prints to console window if console it attached
                game_console.print(consoletext)
            else:
                print(consoletext)
            self.remove_message_candidate(tags['console'])
        # redraws hover message
        if ('hover' in self.venues):
            self.hover_box.rewrite_text(messages['hover'][1], messages['hover'][2])


class GameInput:
    def key_detect(event):
        foo = event.char
        if foo == 'q':
            game_object.player1.set_move(0)
        elif foo == 'w':
            game_object.player1.set_move(1)
        elif foo == 'e':
            game_object.player1.set_move(2)

    def space_detect(event):
        pass
        # game_object.player1.cycle_move()

    def leftKey(event):
        GameInput.try_move(m_c.WEST)

    def rightKey(event):
        GameInput.try_move(m_c.EAST)

    def upKey(event):
        GameInput.try_move(m_c.NORTH)

    def downKey(event):
        GameInput.try_move(m_c.SOUTH)

    def try_move(dir):
        game_object.player1.move_arrow(dir)
