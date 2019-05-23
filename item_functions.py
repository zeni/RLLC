import tcod as libtcod

from game_messages import Message
from components.plant import Plant

def add_osc(*args, **kwargs):
    entity = args[0]
    freq = kwargs.get('freq')

    results = []
    results.append({'consumed': True, 'message': Message(
        'You drank the oscia potion.', libtcod.violet)})
    entity.type.add_osc(freq)

    return results


def cast_mute(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    maximum_range = kwargs.get('maximum_range')
    results = []
    target = None
    closest_distance = maximum_range + 1
    for entity in entities:
        if entity.type and not isinstance(entity.type,Plant) and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)
            if distance < closest_distance:
                target = entity
                closest_distance = distance
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
            'A force fist crushes the throat of the {0}, rendering it mute !'.format(target.name))})
        target.type.sound.stop()
        target.type.mute = True
    else:
        results.append({'consumed': False, 'target': None, 'message': Message(
            'No enemy is close enough to strike.', libtcod.red)})
    return results

def cast_mute_balls(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    print("mute balls")
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.red)})
        return results
    results.append({'consumed': True, 'message': Message('The mute balls rain, muting everything within {0} tiles!'.format(radius), libtcod.orange)})
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.type and not isinstance(entity.type,Plant):
            results.append({'message': Message('The {0} is muted.'.format(entity.name), libtcod.orange)})
            entity.type.sound.stop()
            entity.type.mute = True
    return results