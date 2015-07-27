__author__ = 'Emilio'

import tkinter as tk
import myconstants as m_c
from player_obj import Player
from world_obj import World_map

from lower_bar import StatBar

from threading import Semaphore

game_object=None

#worldname = "tt" #tile test
#worldname = "kf" #killing floor
#worldname = "ev" #empty void
#worldname = "so" #shootout

#world = World_map(worldname)

class Game:
    def __init__(self, master):
        global game_object
        game_object = self
        #setup window
        self.master = master
        master.wm_title("Punch Arena v." + m_c.VERSION_NUMBER)
        #create state machine core
        self.my_state = StateCore()
        #create message core
        self.my_msg = MessageCore()
        #create time core (animation, state machine update)
        self.my_time = TimeCore(master,self.my_state,self.my_msg)
        #setup canvases
        map_canvas = tk.Canvas(master,bg = 'pink', width=m_c.canvas_w, height=m_c.canvas_h1,highlightthickness=0)
        map_canvas.pack()
        self.game_arena = World_map(self.my_time, self.my_msg, map_canvas,'tt')
        self.place_player_char(map_canvas)

        statbar_frame = tk.Frame(master,bg = 'red', width=m_c.canvas_w, height=m_c.canvas_h2,highlightthickness=0)
        statbar_frame.pack()
        self.statbar=StatBar(statbar_frame,self.my_time,self.my_msg, self.player1)


        #bind listeners
        master.bind("<space>",GameInput.space_detect)
        master.bind('<Left>', GameInput.leftKey)
        master.bind('<Right>', GameInput.rightKey)
        master.bind('<Up>', GameInput.upKey)
        master.bind('<Down>', GameInput.downKey)
        master.bind('<KeyPress>',GameInput.key_detect)
        self.my_time.start_game_ticks()

    def place_player_char(self, map_canvas):
        #create player
        self.player1 = Player("player1",self.my_time)
        #associate player with canvas, create sprite, and register for animation
        self.player1.attach_canvas(map_canvas)
        self.player1.create_sprite("player1")
        self.player1.register_object()
        #this object DOES need access to the game state machine
        self.player1.attach_state_machine(self.my_state)
        self.player1.attach_worldmap(self.game_arena)
        self.player1.attach_message_core(self.my_msg)
        self.player1.set_coords(self.game_arena.playerPos[0], self.game_arena.playerPos[1])

class TimeCore:
    def __init__(self, tkinter_master, state_core, msg_core, tick_mod=10000):
        self.master = tkinter_master
        self.state_core = state_core
        self.msg_core = msg_core
        #initialize blank list of animation objects
        self.anim_objects = []
        #tick_mod is a constant number for "clocking" events
        self.tick_num = 0
        self.tick_mod = tick_mod #10k by default
        #blocking animation semaphore and count
        self.blocking_anims = 0
        self.blocking_sem = Semaphore()

    def add_anim_actor(self,anim_actor):
        #register actor onto object animation list
        if anim_actor not in self.anim_objects:
            self.anim_objects.append(anim_actor)

    def del_anim_actor(self,anim_actor):
        #remove actor object from animation list
        if anim_actor in self.anim_objects:
            self.anim_objects.remove(anim_actor)

    def start_game_ticks(self):
        self.master.after(m_c.ANIM_START_DELAY,self.tick)
        self.state_core.finish_setup()

    def tick(self):
        for o in self.anim_objects:
            o.animate_tick();
        self.msg_core.play_messages()
        self.master.after(m_c.ANIM_DT,self.tick)

    def animation_blocked(self):
        probe = True
        self.blocking_sem.acquire()
        probe = (self.blocking_anims > 0)
        self.blocking_sem.release()
        return probe

class StateCore:
    valid_states = ('setup','player_turn','in_turn_wait',
                    'pre_turn_wait','change_players','endgame','error')

    def __init__(self):
        self.state = 'setup'
        self.player = 1

    def check_state(self):
        if self.state not in StateCore.valid_states:
            self.state = 'error'
        return self.state

    def player_can_move(self, num):
        #creates concept of "turns
        return (self.state == 'player_turn') & (self.player == num)

    def finish_setup(self):
        self.state = 'player_turn'

    def win_game(self):
        self.state = 'endgame'

class MessageCore:
    VENUES = ['console']

    def __init__(self):
        self.tag_list = []
        self.messages = dict()

    def add_message_candidate(self,tag,packet):
        self.tag_list.append(tag)
        self.messages[tag] = packet

    def remove_message_candidate(self,tag):
        self.tag_list.remove(tag)
        del self.messages[tag]

    def elect_messages(self):
        winners = dict()
        for venue in MessageCore.VENUES:
            winners[venue] = ['','',-1,0,False] #blank packet
            for tag in self.messages.keys():
                if self.messages[tag][0] == venue:
                    try_packet = self.messages[tag]
                    if try_packet[3] > winners[venue][2]:
                        winners[venue] = try_packet
        return winners

    def play_messages(self):
        messages = self.elect_messages()
        if not (messages['console'][2] == -1): #eliminates blank messages
            if (messages['console'][5] == False): #marks message as read to avoid unnecessary message echoing
                print("------CONSOLE MESSAGE-------")
                print(messages['console'][1] + ":")
                print(messages['console'][2])
                messages['console'][5] =True









class GameInput:

    def key_detect(event):
        print("detected " + event.char)

    def space_detect(event):
        game_object.player1.cycle_move()

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
