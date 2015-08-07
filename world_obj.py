import tkinter as tk

import worldData as wd
import myconstants as m_c
from animatable import ProtoAnim

from player_obj import Player
import playerData as pd

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
        self.replace_tile(x, y, new_type)

    def player_broke_tile(self, obj):
        x = obj.next_x
        y = obj.next_y
        self.degrade_tile(x, y)

    def service_tile(self, x, y, obj):
        variant = self.mapData[y][x]
        variant = wd.TILE_LIB[variant][1]
        variant = variant.lower()
        getattr(self, "service_" + variant)(obj)

    def service_err(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.PUNCH:
                self.player_broke_tile(obj)
                obj.add_effect("errconfused")

    def service_floor(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.WALK:
                if obj.has_effect("wetfeet"):
                    x = obj.x
                    y = obj.y
                    map_tiles[y][x].send_to_console(str(x) + "," + str(y) + ":", "plop!\n", val=2)
                    self.replace_tile(x, y, wd.PUDDLE)
                    obj.rm_effect("wetfeet")

    def service_wall(self, obj=None):
        if type(obj) is Player:
            pass

    def service_pglass(self, obj=None):
        if type(obj) is Player:
            pass

    def service_sand(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.GRAB:
                obj.add_hand_effect("handsand")
            if mode not in [pd.PUNCH]:
                for effect in pd.FOOT_EFFECTS:
                    obj.rm_effect(effect)

    def service_woodc(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.PUNCH:
                self.player_broke_tile(obj)

    def service_woodb(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.PUNCH:
                self.player_broke_tile(obj)

    def service_wooda(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.WALK:
                self.service_floor(obj)
            if mode is pd.GRAB:
                obj.add_hand_effect("handwood")
                x = obj.x
                y = obj.y
                self.replace_tile(x, y, wd.FLOOR)

    def service_glassc(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.PUNCH:
                self.player_broke_tile(obj)

    def service_glassb(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.PUNCH:
                self.player_broke_tile(obj)

    def service_glassa(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.WALK:
                self.service_floor(obj)
            if mode is pd.GRAB:
                obj.add_hand_effect("handglass")
                x = obj.x
                y = obj.y
                self.replace_tile(x, y, wd.FLOOR)

    def service_lava(self, obj=None):
        if type(obj) is Player:
            x = obj.x
            y = obj.y
            mode = obj.mode
            if mode is pd.WALK:
                if obj.has_effect("wetfeet"):
                    self.replace_tile(x, y, wd.OBSIDIAN)
                    map_tiles[y][x].send_to_console(str(x) + "," + str(y) + ":", "sizzle!\n", val=2)
                    obj.rm_effect("wetfeet")
                    obj.rm_effect("dampfeet")
                    map_tiles[y][x].send_to_console(obj.name + " cooled the lava without incident.", val=2)
                elif obj.has_effect("dampfeet"):
                    self.replace_tile(x, y, wd.OBSIDIAN)
                    map_tiles[y][x].send_to_console(str(x) + "," + str(y) + ":", "sizzle!\n", val=2)
                    obj.rm_effect("dampfeet")
                    map_tiles[y][x].send_to_console(obj.name + " cooled the lava but was singed.", val=2)
                    obj.add_effect("hotfeet")
                    obj.drain_hp(1)
                else:
                    map_tiles[y][x].send_to_console(obj.name + " got burned!", val=2)
                    obj.add_effect("hotfeet")
                    obj.drain_hp(3)
            if mode is pd.GRAB:
                map_tiles[y][x].send_to_console(obj.name + " got burned!", val=2)
                obj.add_effect("hotfeet")
                obj.add_hand_effect("handlava")
            if mode in [pd.BLOCK]:
                map_tiles[y][x].send_to_console(obj.name + " got burned!", val=2)
                obj.add_effect("hotfeet")

    def service_puddle(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if obj.has_effect("hotfeet"):
                x = obj.x
                y = obj.y
                map_tiles[y][x].send_to_console(str(x) + "," + str(y) + ":", "sizzle!\n", val=2)
                self.replace_tile(x, y, wd.FLOOR)
                obj.rm_effect("hotfeet")
            elif obj.has_effect("wetfeet"):
                pass
            else:
                obj.add_effect("dampfeet")
            if mode is pd.GRAB:
                obj.add_hand_effect("handwet")

    def service_water(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            obj.add_effect("wetfeet")
            obj.rm_effect("hotfeet")
            obj.rm_effect("dampfeet")
            if mode is pd.GRAB:
                obj.add_hand_effect("handwet")
            if mode in [pd.WALK, pd.BLOCK, pd.GRAB]:
                #you can't swim! punish them!
                obj.drain_hp(1)

    def service_obs(self, obj=None):
        if type(obj) is Player:
            mode = obj.mode
            if mode is pd.GRAB:
                obj.add_hand_effect("handpeb")

    def replace_tile(self, x, y, variant):
        self.mapData[y][x] = variant
        map_tiles[y][x].repaint_tile(variant)


class mapTile(ProtoAnim):
    """the animated part of a tile--image frames and whatnot"""
    CONSOLE_DETAIL = m_c.WORLD_CONSOLE_DETAIL

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
