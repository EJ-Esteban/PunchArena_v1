# animation constants
PLAYER_ANIM_DELAY = 6
PLAYER_ANIM_DELAY_LONG = 12

# player moves
WALK = 0
BLOCK = 1
PUNCH = 2
HIGH_MOVE = PUNCH

# Dictionary of player moves
# (internal_name,
# bigtext, smalltext)
MOVELIST = dict()
MOVELIST[WALK] = ('walk',
                  'Move (Q)', "Walk around the tiles, all fancy-like")
MOVELIST[BLOCK] = ('block',
                   "Block (W)", "Brace yourself to reduce injuries from a certain direction")
MOVELIST[PUNCH] = ('punch',
                   "Punch (E)", "Agress enemies and map tiles")

VALID_EFFECTS = dict()
VALID_EFFECTS["wetfeet"] = ("Wet Feet",
                            "Your shoes are quite wet.", "blue")
VALID_EFFECTS["dampfeet"] = ("Damp Feet",
                             "Your shoes are a bit wet.", "light blue")
VALID_EFFECTS["hotfeet"] = ("Hot Feet",
                            "Your shoes are quite hot.", "dark orange")
VALID_EFFECTS["blocking"] = ("Blocking",
                             "You are braced for impact!", "dark red")
