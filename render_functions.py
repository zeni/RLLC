# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:00:04 2019

@author: Stephane Perrin
"""

import tcod as libtcod
from game_states import GameStates
from menus import inventory_menu
from constants import COLORS, CAMERA_HEIGHT, CAMERA_WIDTH, MAP_HEIGHT, MAP_WIDTH
from enum import Enum
from map_objects.camera import Camera


class RenderOrder(Enum):
    ITEM = 1
    ENTITY = 2


def render_all(con, panels, entities, player, game_map, fov, message_log, game_state, camera):
    camera.move_camera(player, fov)
    if fov.recompute:
        fov.recompute = False
        fov.recompute_fov(player)
        libtcod.console_clear(con)
        for y in range(camera.height):
            for x in range(camera.width):
                (map_x, map_y) = (int(camera.x + x), int(camera.y + y))
                visible = libtcod.map_is_in_fov(fov.map, map_x, map_y)
                wall = game_map.tiles[map_x][map_y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, COLORS.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, COLORS.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[map_x][map_y].explored = True
                elif game_map.tiles[map_x][map_y].explored:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, COLORS.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, COLORS.get('dark_ground'), libtcod.BKGND_SET)
    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov.map, camera)
    libtcod.console_blit(con, 0, 0, con.width, con.height, 0, 0, 0)
    for panel in panels:
        panel.draw(message_log)
    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(con, player.inventory, 50)


def clear_all(con, panels, entities, camera):
    for entity in entities:
        clear_entity(con, entity, camera)
    for panel in panels:
        libtcod.console_clear(panel)


def draw_entity(con, entity, fov_map, camera):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        (x, y) = camera.to_camera_coordinates(entity.x, entity.y)
        if x is not None:
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char(con, x, y,
                                        entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity, camera):
    # erase the character that represents this object
    (x, y) = camera.to_camera_coordinates(entity.x, entity.y)
    if x is not None:
        libtcod.console_put_char(
            con, x, y, ' ', libtcod.BKGND_NONE)
