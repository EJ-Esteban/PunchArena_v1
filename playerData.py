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
