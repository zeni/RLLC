# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:35:10 2019

@author: Stephane Perrin
"""

import tcod as libtcod
from game_states import GameStates

def handle_player_turn_keys(key):
    # Movement keys
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_inventory_keys(key):
    index = key.c - ord('a')
    if index >= 0:
        return {'inventory_index': index}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}
    return {}

def handle_intro_keys(key):
    index = key.c - ord('a')
    if index >= 0:
        return {'choice': index}
    return {}

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.SHOW_INVENTORY:
        return handle_inventory_keys(key)
    elif game_state == GameStates.INTRO_SCREEN:
        return handle_intro_keys(key)
    elif game_state == GameStates.CLASS_CHOICE:
        return handle_intro_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)
    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    return {}