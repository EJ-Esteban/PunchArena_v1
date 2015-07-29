import myconstants as m_c

class ProtoAnim:
    CONSOLE_DETAIL = -1
    def __init__(self, name, my_time):
        # all animated objects need a name (string) and time core (for animation)
        self.name = name
        self.my_time = my_time
        self.my_canvas = None
        self.anim_frame = 0

        self.console_count = 0
        # animation ticks
        self.tick_til = 0
        self.tick = 0

    def attach_canvas(self, canvas=None):
        # attaches a canvas to the item for drawing
        pass

    def attach_state_machine(self, game_state):
        self.game_state = game_state

    def register_object(self):
        # registers object onto animation list
        self.my_time.add_anim_actor(self)

    def unregister_object(self):
        # removes/freezes object from animation list
        self.my_time.del_anim_actor(self)

    def animate_tick(self):
        # blank method, generally forces a redraw for object
        pass

    def attach_message_core(self, msg_pipe):
        self.msg_tag = "blank"
        self.msg_packet = ["console", "bigtext", "smalltext", 1, 0, False]
        self.msg_pipe = msg_pipe
        self.bind_listeners()

    def bind_listeners(self):
        # blank method, use it to bind specific listener messages
        pass

    def console_ready(self, val):
        return m_c.MASTER_CONSOLE and val <= self.CONSOLE_DETAIL

    def send_to_console(self, text1, text2="", val=5):
        #generic printable for console feedback
        if self.console_ready(val):
            console_packet = ['console', text1, text2, m_c.PRIO_TOP, 0, False]
            self.console_count += 1
            if hasattr(self, 'msg_pipe'):
                self.msg_pipe.add_message_candidate(self.msg_tag + "_Cmsg_" + str(self.console_count), console_packet)
            else:
                print(text1)
                print(text2)
