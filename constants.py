import tcod

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 80
CAMERA_WIDTH = 86
CAMERA_HEIGHT = 70
MAP_WIDTH = 150
MAP_HEIGHT = 130
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_MONSTERS_ROOM = 3
MAX_ITEMS_ROOM = 2
MAX_PLANTS_ROOM = 2
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 5
LIMIT_FPS = 20
COLORS = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150),
    'light_wall': tcod.Color(130, 110, 50),
    'light_ground': tcod.Color(200, 180, 50),
}
