import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from map_objects.fov import FOV
from render_functions import clear_all, render_all
from panel import Panel
from map_objects.game_map import GameMap
from game_messages import MessageLog,Message
from game_states import GameStates
from components.noiseur import Noiseur
from pyo import *


def main():
    SCREEN_WIDTH = 100
    SCREEN_HEIGHT = 80
    MAP_WIDTH = 85
    MAP_HEIGHT = 70
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30
    MAX_MONSTERS_ROOM=3
    FOV_ALGO = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 5
    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50),
    }
    s=Server(duplex=0).boot()
    s.start()
    component = Noiseur(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player',s,
                    blocks=True,type=component)
    player.set_sound(Noise())
    player.sound.out()
    entities = [player]
    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                           "RLLC v0.0", renderer=tcod.RENDERER_SDL2, order="F")
    con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    con.default_fg = tcod.white
    panels = []
    panel = Panel(0, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT-MAP_HEIGHT,"panel")
    panels.append(panel)
    panel = Panel(MAP_WIDTH, 0, SCREEN_WIDTH-MAP_WIDTH, MAP_HEIGHT,"sidebar")
    panels.append(panel)
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE,
                      MAP_WIDTH, MAP_HEIGHT, player,entities,MAX_MONSTERS_ROOM,s)
    fov = FOV(game_map, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
    message_log=MessageLog(2,SCREEN_WIDTH-4,SCREEN_HEIGHT-MAP_HEIGHT)
    key = tcod.Key()
    mouse = tcod.Mouse()
    game_state = GameStates.PLAYERS_TURN
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        fov.recompute_fov(player)
        render_all(con, panels, entities, game_map, fov, message_log, mouse, colors)
        tcod.console_flush()
        clear_all(con, panels, entities)
        action = handle_keys(key)
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        player_turn_results = []
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    player_turn_results.append({'message':Message('You kick the ' + target.name + ' in the shins, much to its annoyance!',tcod.yellow)})
                else:
                    player.move(dx, dy)
                    player_turn_results.append({'message':Message('You moved!',tcod.yellow)})
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            if message:
                message_log.add_message(message)
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results =entity.ai.take_turn(player, entity, fov, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        if message:
                            message_log.add_message(message)   
            else: 
                game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
