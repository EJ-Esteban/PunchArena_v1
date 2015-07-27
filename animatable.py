
class ProtoAnim:
    def __init__(self,name,my_time):
        #all animated objects need a name (string) and time core (for animation)
        self.name = name
        self.my_time = my_time
        self.my_canvas = None
        self.anim_frame = 0

        #animation ticks
        self.tick_til = 0
        self.tick = 0

    def attach_canvas(self,canvas=None):
        #attaches a canvas to the item for drawing
        pass

    def attach_state_machine(self,game_state):
        self.game_state = game_state

    def register_object(self):
        #registers object onto animation list
        self.my_time.add_anim_actor(self)

    def unregister_object(self):
        #removes/freezes object from animation list
        self.my_time.del_anim_actor(self)

    def animate_tick(self):
        #blank method, generally forces a redraw for object
        pass

    def attach_message_core(self,msg_pipe):
        self.msg_tag = "blank"
        self.msg_packet = ["console", "bigtext","smalltext",1,0,False]
        self.msg_pipe = msg_pipe
        self.bind_listeners()

    def bind_listeners(self):
        #blank method, use it to bind specific listener messages
        pass


