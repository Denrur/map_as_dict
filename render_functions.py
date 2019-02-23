from bearlibterminal import terminal as blt
# import time


def render_all(game_map, camera, player, entities, items, corpses, fov_cells):
    terrain = game_map.terrain
    water = game_map.water
    camera.move_camera(player.x, player.y, game_map)
    # print('Camera x: ' + str(camera.x))
    # print('Camera y: ' + str(camera.y))
    # start = time.time()

    for x in range(camera.width):
        for y in range(camera.height):
            map_x, map_y = camera.to_map_coordinates(x, y)
            if (map_x, map_y) in fov_cells:
                if (map_x, map_y) in water:
                    render_obj((map_x, map_y), water, camera, 'blue')
                    water.get((map_x, map_y)).explored = True
                elif (map_x, map_y) in terrain:
                    render_obj((map_x, map_y), terrain, camera, 'gray')
                    terrain.get((map_x, map_y)).explored = True
                else:
                    blt.puts(x, y, '[color=yellow].')

                if (map_x, map_y) in corpses:
                    obj = corpses.get((map_x, map_y))
                    render_obj((map_x, map_y), corpses, camera, obj.color)

                if (map_x, map_y) in items:
                    obj = items.get((map_x, map_y))
                    render_obj((map_x, map_y), items, camera, obj.color)

                if (map_x, map_y) in entities:
                    obj = entities.get((map_x, map_y))
                    render_obj((map_x, map_y), entities, camera, obj.color)
            elif ((map_x, map_y) in terrain and
                  terrain.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), terrain, camera, 'darker orange')
            elif ((map_x, map_y) in water and
                  water.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), water, camera, 'darker blue')


def render_obj(coords, dic, camera, color):
    cam_x, cam_y = camera.to_camera_coordinates(coords[0], coords[1])
    map_x, map_y = coords
    blt.color(color)
    blt.puts(cam_x, cam_y, dic.get((map_x, map_y)).char)
    blt.color('white')
