# from noie_map import NoiseMap
from entity import Entity
import noise
from place_entities import place_entities
import itertools
from random import randint


def generate_chunk(x, y, size, game_map, entities, items,
                   max_monsters, max_items):

    assert x % size == 0
    assert y % size == 0

    if (x, y) in game_map.chunks:
        return

    game_map.chunks.add((x, y))
    max_noise = float('-inf')
    min_noise = float('inf')
    scale = 10
    octaves = 5
    persistance = 0.3
    lactunarity = 1.1
    height_map = dict()
    for j in range(x, x + size):
        for k in range(y, y + size):
            # print(j, k)
            noise_value = noise.snoise2(j/scale, k/scale,
                                        octaves,
                                        persistance,
                                        lactunarity)

            if noise_value > max_noise:
                max_noise = noise_value
            elif noise_value < min_noise:
                min_noise = noise_value
            height_map[(j, k)] = noise_value

    for (j, k) in height_map:
        height_map[(j, k)] = (height_map[(j, k)] - min_noise)/(
            max_noise - min_noise)

        if height_map[(j, k)] < 0.1:
            game_map.water[(j, k)] = Entity(j, k, '[U+504A]', 'white', 'water')
        elif height_map[(j, k)] < 0.7:
            pass
        elif height_map[(j, k)] < 1:
            walls = ['[U+2140]', '[U+2141]', '[U+2142]']
            r = randint(0, 2)
            game_map.terrain[(j, k)] = Entity(j, k, walls[r], 'white', 'wall')
    # print("size ", size)
    place_entities(x, y, size, entities, items, game_map,
                   max_monsters, max_items)


def add_new_chunks(cx, cy, chunk_size, game_map, entities, items,
                   max_monsters, max_items):

    for x, y in itertools.product([cx - chunk_size, cx, cx + chunk_size],
                                  [cy - chunk_size, cy, cy + chunk_size]):
        generate_chunk(x, y, chunk_size, game_map, entities, items,
                       max_monsters, max_items)
