import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from map_objects.fov import FOV
from render_functions import clear_all, render_all
from panel import Panel
from map_objects.game_map import GameMap
from game_messages import MessageLog, Message
from game_states import GameStates
from components.noiseur import Noiseur
from components.inventory import Inventory
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT, MAP_WIDTH
from pyo import *


def main():
    # start pyo server
    pyo_server = Server(duplex=0).boot()
    pyo_server.start()
    # create player
    # TODO add different classes
    player = Entity(0, 0, '@', tcod.white, 'Player',
                    blocks=True, type=Noiseur(sound=Noise()), inventory=Inventory(20))
    player.type.sound_out()
    entities = [player]
    # some initializations, main console
    # TODO add a spectrum analyser panel ?
    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                           "RLLC v0.0", renderer=tcod.RENDERER_SDL2, order="F")
    con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    con.default_fg = tcod.white
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    # create sub-panels
    panels = []
    panel = Panel(0, MAP_HEIGHT, SCREEN_WIDTH,
                  SCREEN_HEIGHT-MAP_HEIGHT, "log")
    panels.append(panel)
    panel = Panel(MAP_WIDTH, 0, SCREEN_WIDTH-MAP_WIDTH, MAP_HEIGHT, "sidebar")
    panels.append(panel)
    message_log = MessageLog(2, SCREEN_WIDTH-4, SCREEN_HEIGHT-MAP_HEIGHT-2)
    # create game map and place entities, fov
    game_map = GameMap()
    game_map.make_map(player, entities)
    fov = FOV(game_map)
    # compute fov
    fov.recompute_fov(player)
    # inputs
    key = tcod.Key()
    mouse = tcod.Mouse()
    # main loop
    while not tcod.console_is_window_closed():
        # get events
        tcod.sys_check_for_event(
            tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        # get action from keyboard
        action = handle_keys(key, game_state)
        move = action.get("move")
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        # deal with actions
        player_turn_results = []
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y)
                if target:
                    player_turn_results.append({'message': Message(
                        'You kick the ' + target.name + ' in the shins, much to its annoyance!', tcod.yellow)})
                else:
                    player.move(dx, dy)
                    player_turn_results.append(
                        {'message': Message('You moved!', tcod.yellow)})
                    # compute fov
                    fov.recompute_fov(player)
            game_state = GameStates.ENEMY_TURN
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(
                    Message('There is nothing here to pick up.', tcod.yellow))
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        if inventory_index is not None and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            player_turn_results.extend(player.inventory.use(item))
        if exit:
            if game_state == GameStates.SHOW_INVENTORY:
                game_state = previous_game_state
            else:
                pyo_server.stop()
                return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            if message:
                message_log.add_message(message)
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                game_state = GameStates.ENEMY_TURN
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, entity, fov, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        if message:
                            message_log.add_message(message)
            else:
                game_state = GameStates.PLAYERS_TURN
        # render everything
        render_all(con, panels, entities, player, game_map,
                   fov, message_log, game_state)
        tcod.console_flush()
        clear_all(con, panels, entities)
        


if __name__ == "__main__":
    main()
