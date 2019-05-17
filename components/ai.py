import tcod as libtcod

from game_messages import Message

class BasicMonster:
    def __init__(self):
        self.owner=None

    def take_turn(self, target, source, fov, game_map, entities):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov.map, monster.x, monster.y):
            if not source.type.sound.isOutputting():
                source.type.sound.out()
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.type.hp > 0:
               results.append({'message':Message('The {0} insults you! Your ego is damaged!'.format(monster.name),libtcod.blue)})
        else:
            if source.type.sound.isOutputting():
                source.type.sound.stop()
        return results

