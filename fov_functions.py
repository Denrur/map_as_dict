def recompute_fov(game_map, x, y, radius, light_walls=True, algorithm=12):
    return game_map.tcod_map.compute_fov(x, y, radius, light_walls, algorithm)
