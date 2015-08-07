__author__ = 'Emilio'

import tkinter as tk
import myconstants as m_c
from player_obj import Player
from world_obj import World_map

from lower_bar import StatBar

import threading

game_object = None
game_console = None


class Game:
    def __init__(self, master):
        global game_object
        game_object = self
        self.launch_game_cores(master)
        self.launch_game_graphics(master, 'tt')
        self.launch_game_listeners(master)
        self.my_time.start_game_ticks()

    def launch_game_cores(self, master):
        # create state machine core
        self.my_state = StateCore()
        # create message core
        self.my_msg = MessageCore(self.my_state)
        self.my_state.attach_message_core(self.my_msg)
        # create time core (animation, state machine update)
        self.my_time = TimeCore(master, self.my_state, self.my_msg)
        self.my_state.attach_time_core(self.my_time)
        self.my_msg.attach_time_core(self.my_time)

    def launch_game_graphics(self, master, arena='tt'):
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
        self.my_msg.create_overhead(map_canvas)

    def place_player_char(self, map_canvas):
        # create player
        self.player1 = Player("player1", self.my_time, NPC=False, pid = 1)
        # associate player with canvas, create sprite, and register for animation
        self.player1.attach_canvas(map_canvas)
        self.player1.create_sprite("player1")
        self.player1.register_object()
        # attaching all the relevant crap
        self.player1.attach_state_machine(self.my_state)
        self.player1.attach_worldmap(self.game_arena)
        self.player1.attach_message_core(self.my_msg)
        self.player1.set_coords(self.game_arena.playerPos[0], self.game_arena.playerPos[1])
        self.my_state.append_player(self.player1)

    def launch_game_listeners(self, master):
        # bind listeners
        master.bind("<space>", GameInput.space_detect)
        master.bind('<Left>', GameInput.leftKey)
        master.bind('<Right>', GameInput.rightKey)
        master.bind('<Up>', GameInput.upKey)
        master.bind('<Down>', GameInput.downKey)
        master.bind('<KeyPress>', GameInput.key_detect)

    def attach_console(self, console):
        global game_console
        game_console = console

    def debug_place_world_tile(self, x, y, variant):
        self.game_arena.replace_tile(x, y, variant)

    def check_time(self):
        return self.my_time.check_time()

    def force_state(self, s):
        self.my_state.set_state(s)


class TimeCore:
    """
    This class manages animation and game ticks, mostly through the tick() method
    """

    def __init__(self, tkinter_master, state_core, msg_core, tick_mod=1200):
        self.master = tkinter_master
        self.state_core = state_core
        self.msg_core = msg_core
        # initialize blank list of animation objects
        self.anim_objects = []
        # tick_mod is a constant number for "clocking" events
        self.tick_epoch = 0  # with default tick mod, it's the number of minutes elapsed
        self.tick_num = 0
        self.tick_mod = tick_mod  # 1.2k (1 minute) by default
        # blocking animation semaphore and count
        self.blocking_anims = 0
        self.msg_lock = threading.Lock()

    def check_time(self):
        a = {'Tick number:': self.tick_num, 'Animation dt:': str(m_c.ANIM_DT) + " ms"}
        s = 'Minute:'
        if not self.tick_mod == 1200:
            s = 'Epoch:'
            a['Tick mod:'] = self.tick_mod
        a[s] = self.tick_epoch
        return a

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
        """creates and calls threads to run animation and state machine updates"""

        # service the state machine at the start of every step
        animation_threads = []
        a = self.state_core.service()
        # play any messages
        self.msg_core.play_messages()
        if a is False:
            return
        # animate any obhects
        for o in self.anim_objects:
            t = threading.Thread(target=o.animate_tick)
            animation_threads.append(t)
            t.start()
        # tick again after
        self.tick_num += 1
        if self.tick_num >= self.tick_mod:
            self.tick_epoch += 1
            self.tick_num = 0
        self.master.after(m_c.ANIM_DT, self.tick)

    def animation_blocked(self):
        self.msg_lock.acquire()
        probe = (self.blocking_anims > 0)
        self.msg_lock.release()
        return probe

    def add_blocking_animation(self):
        self.msg_lock.acquire()
        self.blocking_anims += 1
        self.msg_lock.release()

    def rm_blocking_animation(self):
        self.msg_lock.acquire()
        self.blocking_anims -= 1
        if self.blocking_anims < 0:
            self.state_core.set_state('error_external')
        self.msg_lock.release()


class StateCore:
    valid_states = (
        'setup', 'player_turn', 'in_turn_wait', 'pre_turn_wait', 'change_players', 'endgame', 'error_check',
        'error_set',
        'error_external'
        , 'freeze')

    def __init__(self):
        self.state = 'setup'
        self.player = 1
        self.state_lock = threading.Lock()
        self.forced = False
        self.my_msg = None
        self.my_time = None

        self.player_list = []
        self.players_dead = []
        self.players_alive = []

        self.turn_forced = False

    def attach_message_core(self, msg):
        self.my_msg = msg

    def attach_time_core(self, time):
        self.my_time = time

    def append_player(self, player_obj):
        if player_obj in self.player_list:
            return False
        self.player_list.append(player_obj)
        self.players_alive.append(player_obj)
        return True

    def kill_player(self, player_obj):
        """returns true if a player is successfully removed from the game"""
        if player_obj not in self.player_list or player_obj not in self.players_alive:
            return False
        self.players_alive.remove(player_obj)
        self.players_dead.append(player_obj)
        return True

    def set_player(self, num):
        self.state_lock.acquire()
        self.player = num
        self.state_lock.release()

    def check_state(self):
        self.state_lock.acquire()
        if self.forced:
            self.state_lock.release()
            return self.state
        if self.state not in StateCore.valid_states:
            self.state = 'error_check'
        self.state_lock.release()
        return self.state

    def set_state(self, s):
        a = True
        self.state_lock.acquire()
        if s not in StateCore.valid_states:
            self.state = 'error_set'
            a = False
        else:
            self.state = s
        self.state_lock.release()
        return a

    def force_turn_end(self):
        self.state_lock.acquire()
        self.turn_forced = True
        self.state_lock.release()

    def check_turn_forced(self):
        self.state_lock.acquire()
        t = self.turn_forced
        self.state_lock.release()
        return t

    def player_can_move(self, num):
        # creates concept of "turns
        s = self.check_state()
        return (s == 'player_turn') & (self.player == num)

    def finish_setup(self):
        self.set_state('player_turn')

    def service(self):
        s = self.check_state()
        if s == 'player_turn':
            self.state_player_turn()
        elif s == 'in_turn_wait':
            self.state_in_turn_wait()
        elif s == 'pre_turn_wait':
            self.state_pre_turn_wait()
        elif s == 'change_players':
            self.state_change_players()
        elif s == 'endgame':
            self.state_endgame()
        elif s == 'freeze':
            return False
        elif s in ['error_check', 'error_set', 'setup']:
            console_packet = ['console', "ERROR: STATE MACHINE HAS ENTERED UNSERVICABLE STATE:", s, m_c.PRIO_TOP, 0,
                              False]
            self.send_to_console(console_packet)
            self.set_state('freeze')
        elif s == 'error_external':
            console_packet = ['console', "ERROR: EXTERNAL ERROR DETECTED", s, m_c.PRIO_TOP, 0,
                              False]
            self.send_to_console(console_packet)
            self.set_state('freeze')
        else:
            # you really should never see this message
            console_packet = ['console', "ERROR: STATE MACHINE NOT IN KNOWN STATE:", s + "\nTHIS SHOULD NEVER HAPPEN",
                              m_c.PRIO_TOP, 0, False]
            self.send_to_console(console_packet)
            self.set_state('freeze')
        return True

    def state_player_turn(self):
        """stuff that happens on a player's turn"""
        # check if game should be ended--all but one player is dead (or game is a draw)
        self.reap_players()
        gameover = self.check_if_winner()

        # move to inturn wait if blocking animation(s) are playing
        blocked = self.my_time.animation_blocked()

        # end turn if end has been forced

        turn_end = self.check_turn_forced()

        if gameover or blocked or turn_end:
            # move to inturn wait until animations end
            self.set_state('in_turn_wait')

    def state_in_turn_wait(self):
        self.reap_players()
        gameover = self.check_if_winner()

        # move to inturn wait if blocking animation(s) are playing
        blocked = self.my_time.animation_blocked()

        if blocked:
            return

        if gameover:
            self.set_state('endgame')

        turn_end = self.check_turn_forced()

        if turn_end:
            self.state_lock.acquire()
            self.turn_forced = False
            self.state_lock.release()
            self.set_state('change_players')
            return

        # by default return to player turn
        self.set_state('player_turn')

    def state_pre_turn_wait(self):
        self.set_state('player_turn')

    def state_change_players(self):
        # this will probably have to be brushed up when more players start appearing
        player_count = len(self.players_alive)
        next_player_num = (self.player + 1) % player_count + 1

        next_player = self.players_alive[next_player_num - 1]
        self.player = next_player_num

        overhead_msg = ['overhead', "player %d's turn!" % next_player_num, "", m_c.PRIO_TOP, 25, False]
        self.my_msg.add_message_candidate('statemachine', overhead_msg)

        next_player.refill_walking()

        self.set_state('pre_turn_wait')

    def state_endgame(self):
        pass

    def reap_players(self):
        """offically kills dead players"""
        for player in self.players_alive:
            hp = player.check_stat("hp")
            max_hp = player.check_stat("max_hp")
            if hp <= 0 or max_hp <= 0:
                # player died due to hp being set to 0
                self.kill_player(player)
            if player.has_effect("unique_dead"):
                # player has been killed by a special kill effect
                self.kill_player(player)

    def check_if_winner(self):
        """checks if there's only one player
        if nobody alive: game ends on a draw:
        (possibly check for players being on teams in the future?)"""

        # right now there's only one dude, so there's not really any winning.
        # return len(self.players_alive) <= 1

        # standing function for if the one player is dead
        return len(self.players_alive) == 0

    def send_to_console(self, console_packet):
        if hasattr(self, 'msg_pipe'):
            self.msg_pipe.add_message_candidate("state_machine_msg", console_packet)
        else:
            print(console_packet[1])
            print(console_packet[2])


class MessageCore:
    def __init__(self, state):
        self.venues = ['console', 'overhead']
        self.tag_list = []
        self.my_state = state
        self.messages = dict()

    def attach_time_core(self, time):
        self.my_time = time

    """create and change the overhead message"""

    def create_overhead(self, canvas):
        self.overhead_canvas = canvas
        s = "Once the game is over, the king and the pawn go back in the same box."
        self.overhead_label = tk.Label(canvas, font="Helvetica 20", fg="black", bg="light gray", state="normal",
                                       justify="center", wraplength=500, text=s, anchor="center", relief="raised")
        canvas.create_window(300, 200, window=self.overhead_label, tag="over")
        self.hide_overhead()

    def hide_overhead(self):
        self.overhead_canvas.itemconfig("over", state="hidden")

    def show_overhead(self):
        self.overhead_canvas.itemconfig("over", state="normal")

    def set_overhead(self, text):
        self.overhead_label.config(text=text)

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
        return winners, winningtag

    def play_messages(self):
        w_messages, w_tags = self.elect_messages()

        # plays leading console message
        if not (w_messages['console'][3] == -1):  # eliminates blank messages
            consoletext = w_messages['console'][1]
            consoletext += "\n" + w_messages['console'][2]
            if game_console:  # prints to console window if console it attached
                game_console.print(consoletext)
            else:
                print(consoletext)
            self.remove_message_candidate(w_tags['console'])

        # draws hover box
        if (w_messages['overhead'][3] == -1):  # hides overhead on blank message
            self.hide_overhead()
        else:
            self.show_overhead()
            overtext = w_messages['overhead']
            overtag = w_tags['overhead']
            self.set_overhead(overtext[1])

            if (overtext[5] == False):
                overtext[5] = True
                self.my_time.add_blocking_animation()

            overtext[3] = m_c.PRIO_PLAYING
            overtext[4] -= 1
            if (overtext[4] <= 0):
                self.my_time.rm_blocking_animation()
                self.remove_message_candidate(overtag)

            else:
                self.messages[overtag] = overtext


        # redraws hover message
        if ('hover' in self.venues):
            self.hover_box.rewrite_text(w_messages['hover'][1], w_messages['hover'][2])


class GameInput:
    def key_detect(event):
        foo = event.char
        player = game_object.player1
        if foo in player.key_map.keys() and player.is_turn():
            player.set_move(player.key_map[foo])

    def space_detect(event):
        game_object.player1.spacebar()

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
