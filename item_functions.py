import tcod as libtcod

from game_messages import Message


def add_osc(*args, **kwargs):
    entity = args[0]
    freq = kwargs.get('freq')

    results = []
    results.append({'consumed': True, 'message': Message('You drank the oscia potion.', libtcod.violet)})
    entity.type.add_osc(freq)

    return results