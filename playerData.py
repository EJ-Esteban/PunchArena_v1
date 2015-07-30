# animation constants
PLAYER_ANIM_DELAY = 6
PLAYER_ANIM_DELAY_LONG = 12

# player moves
WALK = 0
PUNCH = 1
BLOCK = 2
GRAB = 3
THROW = 4
HIGH_MOVE = BLOCK

# Dictionary of player moves
# (internal_name,
# bigtext, smalltext)
MOVELIST = dict()
# elementary moves
MOVELIST[WALK] = ('walk', 'movebutton',
                  'Move (Q)', "Walk around the tiles, all fancy-like. (arrows)")
MOVELIST[BLOCK] = ('block', 'blockbutton',
                   "Block (W)", "Brace yourself to reduce incoming injuries. (arrows)")
MOVELIST[PUNCH] = ('punch', 'punchbutton',
                   "Punch (E)", "Agress enemies and map tiles. (arrows)")
MOVELIST[GRAB] = ('grab', 'grabbutton',
                  "Grab (R)", "Pick up debris (space) or grab nearby enemies (arrows). ")
MOVELIST[THROW] = ('throw', 'throwbutton',
                   "Throw (R)", "Toss an enemy in a direction")


VALID_EFFECTS = dict()
# elementary effects
VALID_EFFECTS["blocking"] = ("Blocking",
                             "You are braced for impact!", "dark red")
VALID_EFFECTS["errconfused"] = ("Confused",
                                "What was that tile you broke!?!?!!", "violet")

#foot effects
FOOT_EFFECTS = ["wetfeet", "dampfeet", "hotfeet"]
VALID_EFFECTS["wetfeet"] = ("Wet Feet",
                            "Your shoes are quite wet.", "blue")
VALID_EFFECTS["dampfeet"] = ("Damp Feet",
                             "Your shoes are a bit wet.", "light blue")
VALID_EFFECTS["hotfeet"] = ("Hot Feet",
                            "Your shoes are quite hot.", "dark orange")

# hand effects
HAND_EFFECTS = ["handpeb", "handlava", "handwet", "handsand", "handwood", "handglass"]
VALID_EFFECTS["handpeb"] = ("Object in Hand",
                           "Your hand is filled with obsidian pebbles.", "dark gray")
VALID_EFFECTS["handlava"] = ("Object in Hand",
                             "Your hand is coated in lava. Also, it's on fire.", "orange")
VALID_EFFECTS["handwet"] = ("Object in Hand",
                           "Your hand is wet. Good for exterminating green witches.", "light blue")
VALID_EFFECTS["handsand"] = ("Object in Hand",
                             "You have a handful of sand.", "yellow")
VALID_EFFECTS["handwood"] = ("Object in Hand",
                           "You're carrying some sharp wooden splinters.", "brown")
VALID_EFFECTS["handglass"] = ("Object in Hand",
                           "You're carrying some sharp glass shards.", "white")
