import tcod as libtcod

class BasicMonster:
    def __init__(self):
        self.owner=None

    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))