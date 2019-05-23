import tcod
import tcod.event
from input_handlers import handle_keys, handle_mouse
from entity import Entity, get_blocking_entities_at_location
from map_objects.fov import FOV
from render_functions import clear_all, render_all, RenderOrder
from panel import Panel
from map_objects.game_map import GameMap
from map_objects.camera import Camera
from game_messages import MessageLog, Message
from game_states import GameStates
from components.noiseur import Noiseur
from components.inventory import Inventory
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_HEIGHT, MAP_WIDTH, CAMERA_HEIGHT, CAMERA_WIDTH, LIMIT_FPS
from menus import main_menu
from pyo import *


def start_screen(con, game_state, key, title):
    # show the game's title, and some credits!
    tcod.console_set_default_foreground(con, tcod.light_yellow)
    tcod.console_print_ex(con, int((SCREEN_WIDTH-len(title))/2),
                          2, tcod.BKGND_NONE, tcod.LEFT, title)
    tcod.console_blit(con, 0, 0, con.width, con.height, 0, 0, 0)
    # show options and wait for the player's choice
    options = ['Play a new game', 'Quit']
    main_menu(options, 75, "Play")
    action = handle_keys(key, game_state)
    choice = action.get('choice')
    gamestate = game_state
    if choice == 1:
        gamestate = GameStates.EXIT
    elif choice == 0:
        gamestate = GameStates.CLASS_CHOICE
    tcod.console_flush()
    return gamestate


def class_choice(con, game_state, key, title):
    # show the game's title, and some credits!
    tcod.console_set_default_foreground(con, tcod.light_yellow)
    tcod.console_print_ex(con, int((SCREEN_WIDTH-len(title))/2),
                          2, tcod.BKGND_NONE, tcod.LEFT, title)
    tcod.console_blit(con, 0, 0, con.width, con.height, 0, 0, 0)
    # show options and wait for the player's choice
    options = ['Noiseur', 'Quit']
    main_menu(options, 75, "Choose class")
    action = handle_keys(key, game_state)
    choice = action.get('choice')
    gamestate = game_state
    if choice == 1:
        gamestate = GameStates.EXIT
    elif choice == 0:
        gamestate = GameStates.PLAYERS_TURN
    tcod.console_flush()
    return gamestate


def main():
     # some initializations, main console
    title = 'NOIGUE L.C.'
    tcod.sys_set_fps(LIMIT_FPS)
    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                           title, renderer=tcod.RENDERER_SDL2, order="F")
    con = tcod.console.Console(MAP_WIDTH, MAP_HEIGHT)
    con.default_fg = tcod.white
    game_state = GameStates.INTRO_SCREEN
    # inputs
    key = tcod.Key()
    mouse = tcod.Mouse()
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(
            tcod.EVENT_KEY_PRESS, key, mouse)
        if game_state == GameStates.INTRO_SCREEN:
            game_state = start_screen(con, game_state, key, title)
        elif game_state == GameStates.EXIT:
            break
        elif game_state == GameStates.CLASS_CHOICE:
            game_state = class_choice(con, game_state, key, title)
        elif game_state == GameStates.PLAYERS_TURN:
            # start pyo server
            pyo_server = Server(duplex=0).boot()
            pyo_server.start()
            # create player
            player = Entity(0, 0, '@', tcod.white, 'Player',
                            blocks=True, type=Noiseur(sound=Noise()), inventory=Inventory(26), render=RenderOrder.ENTITY)
            player.type.sound_out()
            entities = [player]
            previous_game_state = game_state
            # create sub-panels
            panels = []
            panel = Panel(0, CAMERA_HEIGHT, SCREEN_WIDTH,
                          SCREEN_HEIGHT-CAMERA_HEIGHT, "log")
            panels.append(panel)
            panel = Panel(CAMERA_WIDTH, 0, SCREEN_WIDTH -
                          CAMERA_WIDTH, CAMERA_HEIGHT, "sidebar")
            panels.append(panel)
            message_log = MessageLog(
                2, SCREEN_WIDTH-4, SCREEN_HEIGHT-CAMERA_HEIGHT-2)
            # create game map and place entities, fov
            camera = Camera()
            game_map = GameMap()
            game_map.make_map(player, entities)
            fov = FOV(game_map)
            # compute fov
            fov.recompute_fov(player)
            # main loop
            targeting_item = None
            while not tcod.console_is_window_closed():
                # get events
                tcod.sys_check_for_event(
                    tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
                # render everything
                render_all(con, panels, entities, player, game_map,
                           fov, message_log, game_state, camera)
                tcod.console_flush()
                clear_all(con, panels, entities, camera)
                # get action from keyboard
                action = handle_keys(key, game_state)
                mouse_action = handle_mouse(mouse)
                move = action.get("move")
                pickup = action.get('pickup')
                show_inventory = action.get('show_inventory')
                if show_inventory:
                    previous_game_state = game_state
                    game_state=GameStates.SHOW_INVENTORY
                inventory_index = action.get('inventory_index')
                exit = action.get("exit")
                fullscreen = action.get("fullscreen")
                left_click = mouse_action.get('left_click')
                right_click = mouse_action.get('right_click')
                # deal with actions
                player_turn_results = []
                if game_state == GameStates.PLAYERS_TURN:
                    if move:
                        dx, dy = move
                        destination_x = player.x + dx
                        destination_y = player.y + dy
                        if not game_map.is_blocked(destination_x, destination_y):
                            target = get_blocking_entities_at_location(
                                entities, destination_x, destination_y)
                            if not target:
                                player.move(dx, dy)
                                fov.recompute = True
                        game_state = GameStates.ENEMY_TURN
                    elif pickup :
                        for entity in entities:
                            if entity.item and entity.x == player.x and entity.y == player.y:
                                pickup_results = player.inventory.add_item(entity)
                                player_turn_results.extend(pickup_results)
                                break
                        else:
                            message_log.add_message(
                                Message('There is nothing here to pick up.', tcod.yellow))
                if game_state == GameStates.SHOW_INVENTORY:
                    if inventory_index is not None and inventory_index < len(player.inventory.items):
                        item = player.inventory.items[inventory_index]
                        player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov.map))
                if game_state == GameStates.TARGETING:
                    if left_click:
                        target_x, target_y = left_click
                        item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov.map,
                                                                target_x=int(target_x+camera.x), target_y=int(target_y+camera.y))
                        player_turn_results.extend(item_use_results)
                    elif right_click:
                        player_turn_results.append({'targeting_cancelled': True})
                for player_turn_result in player_turn_results:
                    message = player_turn_result.get('message')
                    item_added = player_turn_result.get('item_added')
                    item_consumed = player_turn_result.get('consumed')
                    targeting = player_turn_result.get('targeting')
                    targeting_cancelled = player_turn_result.get('targeting_cancelled')
                    if message:
                        message_log.add_message(message)
                    if item_added:
                        entities.remove(item_added)
                        game_state = GameStates.ENEMY_TURN
                    if item_consumed:
                        game_state = GameStates.ENEMY_TURN
                    if targeting:
                        previous_game_state = GameStates.PLAYERS_TURN
                        game_state = GameStates.TARGETING
                        targeting_item = targeting
                        message_log.add_message(targeting_item.item.targeting_message)
                    if targeting_cancelled:
                        game_state = previous_game_state
                        message_log.add_message(Message('Targeting cancelled'))
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
                if exit:
                    if game_state == GameStates.SHOW_INVENTORY:
                        game_state = previous_game_state
                    elif game_state == GameStates.TARGETING:
                        player_turn_results.append({'targeting_cancelled': True})
                    else:
                        pyo_server.stop()
                        return True
                if fullscreen:
                    tcod.console_set_fullscreen(
                        not tcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
