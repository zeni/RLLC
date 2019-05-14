# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:06:54 2019

@author: Stephane Perrin
"""

from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles
    
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False