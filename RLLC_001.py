import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity
from map_objects.fov import FOV
from render_functions import clear_all, render_all
from panel import Panel
from map_objects.game_map import GameMap
from pyo import *


def main():
    SCREEN_WIDTH = 100
    SCREEN_HEIGHT = 80
    MAP_WIDTH = 85
    MAP_HEIGHT = 70
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30
    FOV_ALGO = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 5
    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50),
    }

    player = Entity(0, 0, '@', tcod.white, 'Player',
                    blocks=True)
    entities = [player]
    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                           "RLLC v0.0", renderer=tcod.RENDERER_SDL2, order="F")
    con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    con.default_fg = tcod.white
    panels = []
    panel = Panel(0, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT-MAP_HEIGHT)
    panels.append(panel)
    panel = Panel(MAP_WIDTH, 0, SCREEN_WIDTH-MAP_WIDTH, MAP_HEIGHT)
    panels.append(panel)
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE,
                      MAP_WIDTH, MAP_HEIGHT, player)
    fov = FOV(game_map, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
    key = tcod.Key()
    mouse = tcod.Mouse()
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        fov.recompute_fov(player)
        render_all(con, panels, entities, game_map, fov, colors)
        tcod.console_flush()
        clear_all(con, panels, entities)
        action = handle_keys(key)
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                fov_recompute = True
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
