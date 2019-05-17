# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:00:04 2019

@author: Stephane Perrin
"""

import tcod as libtcod
from game_states import GameStates
from menus import inventory_menu

def render_all(con, panels, entities, player, game_map, fov, message_log, mouse, colors, game_state):
    if fov.recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov.map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov.map)
    libtcod.console_blit(con, 0, 0, con.width, con.height, 0, 0, 0)
    for panel in panels:
        panel.draw(message_log,get_names_under_mouse(mouse, entities, fov))
    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(con, 'Press the key next to an item to use it, or Esc to cancel.\n',
                       player.inventory, 50, con.width, con.height)


def get_names_under_mouse(mouse, entities, fov):
    (x, y) = (mouse.cx, mouse.cy)
    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov.map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def clear_all(con, panels, entities):
    for entity in entities:
        clear_entity(con, entity)
    for panel in panels:
        libtcod.console_clear(panel)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y,
                                 entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
