import tkinter as tk

import worldData as wd
import myconstants as m_c
from animatable import ProtoAnim

CONSOLE = m_c.MASTER_CONSOLE & m_c.WORLD_CONSOLE
map_tiles = [[0 for y in range(12)] for x in range(8)]


class World_map:
    def __init__(self, my_time, my_msg, my_canvas, worldName='kf'):
        self.my_time = my_time
        self.my_msg = my_msg
        self.my_canvas = my_canvas
        self.load_world(worldName)

    def load_world(self, worldName='kf'):
        # init defaults to killing floor
        try:
            self.worldset = eval("wd." + worldName)
        except AttributeError:
            print("world not found, using KillingFloor")
            self.worldset = wd.kf
        self.mapName = self.worldset['name']
        self.mapData = self.worldset['map']
        self.playerPos = self.worldset['player']
        # populate tile objects
        for y in range(8):
            for x in range(12):
                if self.mapData[y][x] not in range(wd.ERROR, wd.BIGGEST_TILE_VAL + 1):
                    self.mapData[y][x] = wd.ERROR  # autofixes any bad values as an er ror
                map_tiles[y][x] = mapTile(x, y, self.my_time)
                map_tiles[y][x].attach_canvas(self.my_canvas)
                map_tiles[y][x].create_tile(self.mapData[y][x])
                map_tiles[y][x].attach_message_core(self.my_msg)

    def can_walk_tile(self, x, y):
        return self.mapData[y][x] in wd.WALKABLE_TILES

    def can_break_tile(self, x, y):
        return self.mapData[y][x] in wd.BREAKABLE_TILES

    def degrade_tile(self, x, y):
        new_type = wd.NEXT_BREAK[self.mapData[y][x]]
        self.mapData[y][x] = new_type
        map_tiles[y][x].repaint_tile(new_type)


class mapTile(ProtoAnim):
    """the animated part of a tile--image frames and whatnot"""

    def __init__(self, x, y, my_time):
        name = 'tile-' + str(x) + "-" + str(y)
        self.x = x
        self.y = y
        ProtoAnim.__init__(self, name, my_time)

        self.anim_frame = 0
        self.images = []

    def attach_canvas(self, canvas=None):
        self.my_canvas = canvas

    def create_tile(self, type):

        # fetch info tuple
        self.info_tuple = wd.TILE_LIB[type]
        # info tuple[0]: display name, [2]: display info
        # [1]: file name
        # [3]: total frames, [4]: tick interval
        framecount = self.info_tuple[3]
        self.images = [None for i in range(framecount)]
        # create blank image array of appropriate length
        for x in range(framecount):
            self.images[x] = tk.PhotoImage(file=m_c.tile_image(self.info_tuple[1] + str(x)))

        self.my_canvas.create_image(self.x * 50, self.y * 50, anchor="nw", image=self.images[0], tag=self.name)

        if framecount > 1:
            self.register_object()
            self.tick_til = self.info_tuple[4]
            # register for animation if frame count exceeds 1

    def repaint_tile(self, type):
        # fetch info tuple
        self.info_tuple = wd.TILE_LIB[type]

        framecount = self.info_tuple[3]
        self.images = [None for i in range(framecount)]
        # create blank image array of appropriate length
        for x in range(framecount):
            self.images[x] = tk.PhotoImage(file=m_c.tile_image(self.info_tuple[1] + str(x)))

        self.my_canvas.itemconfig(self.name, image=self.images[0])

        if framecount > 1:
            self.register_object()
            self.tick_til = self.info_tuple[4]
            # register for animation if frame count exceeds 1
        else:
            self.unregister_object()
            # make sure it's not in animation queue!

    def animate_tick(self):
        """forces animate on tick"""
        self.tick += 1
        if self.tick >= self.tick_til:
            self.animate()

    def animate(self):
        self.anim_frame += 1
        self.anim_frame %= self.info_tuple[3]
        self.my_canvas.itemconfig(self.name, image=self.images[self.anim_frame])
        self.tick = 0

    def bind_listeners(self):
        self.msg_tag = self.name
        self.my_canvas.tag_bind(self.name, "<Enter>", self.hover_in)
        self.my_canvas.tag_bind(self.name, "<Leave>", self.hover_out)

    def hover_in(self, event):
        self.msg_packet = ['hover', self.info_tuple[0], self.info_tuple[2], m_c.PRIO_HOVER_BACK, 0, False]
        self.msg_pipe.add_message_candidate(self.msg_tag, self.msg_packet)

    def hover_out(self, event):
        self.msg_pipe.remove_message_candidate(self.msg_tag)
