"""
worldData.py
holds dictionaries with world data including maps and walkable types
"""
# basic type flags
ERROR = -1  # error tile, acts like cracked wood
FLOOR = 0  # generic blank tile
WALL = 1  # indestructible wall
PLEXIGLASS = 2  # indestructible glass-can shoot through
SAND = 3  # unshootable, can walk
WOOD = 4  # impasssable, degrades to cracked wood
WOOD_CRACKED = 5  # impassable, degrades to missing wood
WOOD_MISSING = 6  # passable floor surrogate
GLASS = 7  # projectile, degrades to cracked glass
GLASS_CRACKED = 8  # projectile, degrades to missing glass
GLASS_MISSING = 9  # passable floor surrogate
LAVA = 10  # LAVA BURNNSSSSSSS
PUDDLE = 11  # this is a puddle
WATER = 12  # water probably drowns you or whatever? maybe after 2 tiles
OBSIDIAN = 13  # floor tile, probably a result of doing something with water and obsidian

BIGGEST_TILE_VAL = OBSIDIAN  # flag for biggest value to check for errors

"""
tile library-for each element:
[0]: display name (bigtext)
[1]: internal name (images, special effect methods)
[2]: display info (smalltext)
[3]: frames ( >1 means tile is animated)
[4]: frame delay (only relevant if animated)
"""
TILE_LIB = dict()
TILE_LIB[ERROR] = (
    "Error", "err", "What is this tile even?!",
    1, 0)
TILE_LIB[FLOOR] = (
    "Floor", "floor", "A boring empty floor tile",
    1, 0)
TILE_LIB[WALL] = (
    "Wall", "wall", "An indestructible titanium wall",
    1, 0)
TILE_LIB[PLEXIGLASS] = (
    "Plexiglass", "pglass", "An indestructible plexiglass window",
    1, 0)
TILE_LIB[SAND] = (
    "Sand", "sand", "Huh. Someone dumped sand all over this tile.",
    1, 0)
TILE_LIB[WOOD] = (
    "Crate", "woodc", "A relatively sturdy wooden crate.",
    1, 0)
TILE_LIB[WOOD_CRACKED] = (
    "Crate", "woodb", "This wooden crate is cracked.",
    1, 0)
TILE_LIB[WOOD_MISSING] = (
    "Floor", "wooda", "There are a bunch of splinters on the floor!",
    1, 0)
TILE_LIB[GLASS] = (
    "Glass", "glassc", "A relatively sturdy glass window.",
    1, 0)
TILE_LIB[GLASS_CRACKED] = (
    "Glass", "glassb", "This glass window is cracked.",
    1, 0)
TILE_LIB[GLASS_MISSING] = (
    "Floor", "glassa", "There are a bunch of glass shards on the floor!.",
    1, 0)
TILE_LIB[LAVA] = (
    "Lava", "lava", "Only an idiot would try walking on lava.",
    2, 15)
TILE_LIB[PUDDLE] = (
    "Puddle", "puddle", "You're a terrible swimmer, but this water's only like 2 inches deep.",
    1, 0)
TILE_LIB[WATER] = (
    "Water", "water", "You're a terrible swimmer. Might wanna stay out of this one.",
    4, 5)
TILE_LIB[OBSIDIAN] = (
    "Obsidian Floor", "obs", "A solid rock floor, but pretty boring all told.",
    1, 0)

# data on what can be walked, shot through, broken
# these floors can be passed
WALKABLE_TILES = (FLOOR, SAND, WOOD_MISSING, GLASS_MISSING, LAVA, PUDDLE, WATER, OBSIDIAN)

PROJECTILE_TILES = (FLOOR, PLEXIGLASS, GLASS, GLASS_CRACKED, GLASS_CRACKED, WOOD_MISSING, LAVA, WATER, PUDDLE, OBSIDIAN)

BREAKABLE_TILES = (WOOD, WOOD_CRACKED, GLASS, GLASS_CRACKED, ERROR)

# breakables dictionary tells what comes next when something breaks
NEXT_BREAK = dict()
NEXT_BREAK[WOOD] = WOOD_CRACKED
NEXT_BREAK[WOOD_CRACKED] = WOOD_MISSING

NEXT_BREAK[GLASS] = GLASS_CRACKED
NEXT_BREAK[GLASS_CRACKED] = GLASS_MISSING
NEXT_BREAK[ERROR] = FLOOR

"""
MAPS START HERE

"""

# empty void
ev = dict()
ev['name'] = "empty void"
ev['map'] = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
ev['player'] = [1, 1]
ev['AI1'] = [7, 11]

# demo all tiles
tt = dict()
tt['name'] = "tile test"
tt['map'] = [
    [0, 1, 2, 0, 0, 0, 4, 0, 7, 0, 0, 0],
    [0, 0, 13, 0, 0, 0, 5, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -1],
]
tt['player'] = [3, 3]
tt['AI1'] = [7, 11]


# killing floor
kf = dict()
kf['name'] = "killing floor"
kf['map'] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
kf['player'] = [1, 1]
kf['AI1'] = [7, 11]

# shootout
so = dict()
so['name'] = ""
so['map'] = [
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 2, 0, 3, 0, 1, 0, 0, 2, 0, 1],
    [1, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 3, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
]
so['player'] = [1, 1]
so['AI1'] = [7, 11]
