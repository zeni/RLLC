import tcod

class FOV:
    def __init__(self,game_map,radius, light_walls=True, algorithm=0):
        self.recompute=True
        self.radius=radius
        self.light_walls=light_walls
        self.algo=algorithm
        self.map = tcod.map_new(game_map.width, game_map.height)
        for y in range(game_map.height):
            for x in range(game_map.width):
                tcod.map_set_properties(self.map, x, y, not game_map.tiles[x][y].block_sight,
                                        not game_map.tiles[x][y].blocked)

    def recompute_fov(self,entity):
        if self.recompute:
            tcod.map_compute_fov(self.map, entity.x, entity.y, self.radius, self.light_walls, self.algo)