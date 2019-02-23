# from noie_map import NoiseMap
from entity import Entity
import noise
from place_entities import place_entities


def generate_chunk(x, y, size, game_map, entities, items,
                   max_monsters, max_items):
    game_map.chunks.add((x, y))
    max_noise_height = float('-inf')
    min_noise_height = float('inf')
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
            if noise_value > max_noise_height:
                max_noise_height = noise_value
            elif noise_value < min_noise_height:
                min_noise_height = noise_value
            height_map[(j, k)] = noise_value
    for (j, k) in height_map:
        normalize_value = (height_map[(j, k)] - min_noise_height)/(
            max_noise_height - min_noise_height)
        # print(normalize_value)
        height_map[(j, k)] = normalize_value
        if normalize_value < 0.1:
            game_map.water[(j, k)] = Entity(j, k, '~', 'blue', 'water')
        elif normalize_value < 0.7:
            pass
        elif normalize_value < 1:
            game_map.terrain[(j, k)] = Entity(j, k, '#', 'grey', 'wall')
    place_entities(x, y, size, entities, items, game_map,
                   max_monsters, max_items)


def add_new_chunks(cx, cy, player, chunk_size, game_map, entities, items,
                   max_monsters, max_items):
    cx_center = cx + chunk_size / 2
    cy_center = cy + chunk_size / 2

    if (player.x > cx_center) and (player.y > cy_center):
        if (cx + chunk_size, cy) not in game_map.chunks:
            generate_chunk(cx + chunk_size, cy, chunk_size, game_map,
                           entities, items, max_monsters, max_items)
        if (cx + chunk_size, cy + chunk_size) not in game_map.chunks:
            generate_chunk(cx + chunk_size, cy + chunk_size,
                           chunk_size, game_map, entities, items,
                           max_monsters, max_items)
        if (cx, cy + chunk_size) not in game_map.chunks:
                generate_chunk(cx, cy + chunk_size, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
    if (player.x > cx_center) and (player.y < cy_center):
        if (cx + chunk_size, cy) not in game_map.chunks:
                generate_chunk(cx + chunk_size, cy, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
        if (cx + chunk_size, cy - chunk_size) not in game_map.chunks:
                generate_chunk(cx + chunk_size, cy - chunk_size,
                               chunk_size, game_map,
                               entities, items, max_monsters, max_items)
        if (cx, cy - chunk_size) not in game_map.chunks:
                generate_chunk(cx, cy - chunk_size, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
    if (player.x < cx_center) and (player.y < cy_center):
        if (cx, cy - chunk_size) not in game_map.chunks:
                generate_chunk(cx, cy - chunk_size, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
        if (cx - chunk_size, cy - chunk_size) not in game_map.chunks:
                generate_chunk(cx + chunk_size, cy + chunk_size,
                               chunk_size, game_map, entities, items,
                               max_monsters, max_items)
        if (cx - chunk_size, cy) not in game_map.chunks:
                generate_chunk(cx - chunk_size, cy, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
    if (player.x < cx_center) and (player.y > cy_center):
        if (cx - chunk_size, cy) not in game_map.chunks:
                generate_chunk(cx - chunk_size, cy, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
        if (cx - chunk_size, cy - chunk_size) not in game_map.chunks:
                generate_chunk(cx + chunk_size, cy + chunk_size,
                               chunk_size, game_map, entities, items,
                               max_monsters, max_items)
        if (cx, cy + chunk_size) not in game_map.chunks:
                generate_chunk(cx, cy + chunk_size, chunk_size, game_map,
                               entities, items, max_monsters, max_items)
