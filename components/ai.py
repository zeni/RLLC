import tcod as libtcod
import math
from constants import FOV_RADIUS

from game_messages import Message

class FollowMonster:
    def __init__(self):
        self.owner=None

    def take_turn(self, target, source, fov, game_map, entities):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov.map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            monster.type.sound.mul=.1*(FOV_RADIUS-monster.distance_to(target))/FOV_RADIUS
            if not monster.type.sound.isOutputting():
                monster.type.sound.out()
        else:
            if monster.type.sound.isOutputting():
                monster.type.sound.stop()
        return results

class FleeMonster:
    def __init__(self):
        self.owner=None

    def take_turn(self, target, source, fov, game_map, entities):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov.map, monster.x, monster.y):
            monster.move_away(target, entities, game_map)
            monster.type.sound.mul=.1*(FOV_RADIUS-monster.distance_to(target))/FOV_RADIUS
            if not monster.type.sound.isOutputting():
                monster.type.sound.out()
        else:
            if monster.type.sound.isOutputting():
                monster.type.sound.stop()
        return results

