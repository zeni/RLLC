from random import randint
import tcod as libtcod
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from entity import Entity
from pyo import *
from components.monster import Monster
from components.plant import Plant
from components.ai import FollowMonster, FleeMonster, ImmobilePlant
from components.item import Item
from item_functions import add_osc
from constants import MAX_MONSTERS_ROOM, MAX_ROOMS, MAX_ITEMS_ROOM, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_HEIGHT, MAP_WIDTH, MAX_PLANTS_ROOM
from render_functions import RenderOrder


class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, player, entities):
        rooms = []
        num_rooms = 0
        for r in range(MAX_ROOMS):
            w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = randint(0, MAP_WIDTH - w - 1)
            y = randint(0, MAP_HEIGHT - h - 1)
            new_room = Rect(x, y, w, h)
            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self.create_room(new_room)
                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        # finally, append the new room to the list
                    self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        # Get a random number of monsters
        number_of_monsters = randint(0, MAX_MONSTERS_ROOM)
        number_of_items = randint(0, MAX_ITEMS_ROOM)
        number_of_plants = randint(0, MAX_PLANTS_ROOM)
        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    component = Monster(sound=Sine(freq=randint(500, 1000)))
                    monster = Entity(x, y, 'o', libtcod.desaturated_crimson,
                                     'Osc', type=component, ai=FleeMonster(), blocks=True, render=RenderOrder.ENTITY)
                else:
                    component = Monster(sound=Sine(freq=randint(2000, 5000)))
                    monster = Entity(x, y, 'S', libtcod.red, 'Shriker',
                                     type=component, ai=FollowMonster(), blocks=True, render=RenderOrder.ENTITY)
                entities.append(monster)
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item(use_function=add_osc, freq=1500)
                item = Entity(x, y, '!', libtcod.violet,
                              'Oscia Potion', item=item_component)
                entities.append(item)
        for i in range(number_of_plants):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                lfo = Sine(freq=4, mul=.02, add=1)
                lf2 = Sine(freq=.25, mul=10, add=30)
                a = Blit(freq=[100, 99.7]*lfo, harms=lf2, mul=.3)
                component = Plant(sound=a)
                item = Entity(x, y, 'p', libtcod.green,
                              'Singing flower', type=component, ai=ImmobilePlant(), blocks=True, render=RenderOrder.ENTITY)
                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
