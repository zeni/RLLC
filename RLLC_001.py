import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.tile import Tile
from map_objects.game_map import GameMap
from pyo import *


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground':tcod.Color(50, 50, 150)
    }
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)
    entities = [npc, player]

    tcod.console_set_custom_font(
        "I:/Perso/python/RLLC/arial10x10.png",
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )
    tcod.console_init_root(
        screen_width, screen_height, "RLLC v0.0", renderer=tcod.RENDERER_SDL2, order="F"
    )
    con = tcod.console.Console(screen_width, screen_height)
    con.default_fg = tcod.white
    game_map = GameMap(map_width, map_height)
    key = tcod.Key()
    mouse = tcod.Mouse()
#    s = Server(duplex=0).boot()
#    s.start()
#    s.amp = 0.1
#    a = Sine(500,mul=.5).out()
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        tcod.console_flush()
        clear_all(con,entities)
        action = handle_keys(key)
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
