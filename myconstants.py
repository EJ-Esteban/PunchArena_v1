import tkinter

#basic stuff
VERSION_NUMBER = "1.0"

#console settings
MASTER_CONSOLE = False
PLAYER_CONSOLE = True
WORLD_CONSOLE = True


#tkinter constants
canvas_w = 600
canvas_h1 = 400
canvas_h2 = 100
bar_w = 150
bar_h = 50

button_w = 50
button_h = 50

hover_w = 150
hover_h = 100

barfonts = "symbol 10"
barnamefont = "helvetica 18 bold"
anchor = tkinter.NW


#tkinter timing constants
ANIM_START_DELAY = 50
ANIM_DT = 50


#game constants
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


#message priorities
PRIO_TOP = 5 #absolute top (
PRIO_MSG_FREEZE = 4 #freezingf message (notifications, etc.)
PRIO_HOVER_FORE = 3 #hover 1 (hovering over a player)
PRIO_HOVER_BACK = 2 #hover 2 (hovering over a map tile, command)
PRIO_NOTHING_SP = 1 #generic uninteresting messages


#pathing
img_path = "./images/map/tile_"
sprite_path = "./images/sprites/"


#helper functions that use constants
def tile_image(name):
    return img_path + name + ".gif"

def sprite_image(name):
    return sprite_path + name + ".gif"