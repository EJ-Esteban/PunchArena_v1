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
                  'Move (Q)', "Walk around the tiles, all fancy-like.")
MOVELIST[BLOCK] = ('block', 'blockbutton',
                   "Block (W)", "Brace yourself to reduce injuries from a certain direction")
MOVELIST[PUNCH] = ('punch', 'punchbutton',
                   "Punch (E)", "Agress enemies and map tiles")
MOVELIST[GRAB] = ('grab', 'grabbutton',
                  "Grab (R)", "Pick up debris (space) or grab enemies (arrows) to wrestle them!. ")
MOVELIST[THROW] = ('throw', 'throwbutton',
                   "Throw (R)", "Toss an enemy in a direction")


VALID_EFFECTS = dict()
VALID_EFFECTS["blocking"] = ("Blocking",
                             "You are braced for impact!", "dark red")

FOOT_EFFECTS = ["wetfeet", "dampfeet", "hotfeet"]
VALID_EFFECTS["wetfeet"] = ("Wet Feet",
                            "Your shoes are quite wet.", "blue")
VALID_EFFECTS["dampfeet"] = ("Damp Feet",
                             "Your shoes are a bit wet.", "light blue")
VALID_EFFECTS["hotfeet"] = ("Hot Feet",
                            "Your shoes are quite hot.", "dark orange")

HAND_FILLED_EFFECTS = ["handpb", "handlv", "handwt", "handsn", "handwd", "handgl"]
VALID_EFFECTS["handpb"] = ("Pebbles in Hand",
                           "Your hand is filled with obsidian pebbles.", "dark gray")
VALID_EFFECTS["handlv"] = ("Lava in Hand",
                           "Your hand is coated in lava. Also, it's on fire.", "dark orange")
VALID_EFFECTS["handwt"] = ("Wet Hand",
                           "Your hand is wet. Good for exterminating green witches.", "light blue")
VALID_EFFECTS["handsn"] = ("Sandy Hand",
                           "You have a handful of sand.", "orange")
VALID_EFFECTS["handwd"] = ("Splinters in Hand",
                           "You're carrying some sharp wooden splinters.", "brown")
VALID_EFFECTS["handgl"] = ("Shards in Hand",
                           "You're carrying some sharp glass shards.", "white")
