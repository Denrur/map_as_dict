from bearlibterminal import terminal as blt
# import time

def render_bar(x, y, width, name, value, max_val, foreground, background):
    bar_width = int(float(value) / max_val * width)

    last_bg = blt.state(blt.TK_BKCOLOR)
    blt.bkcolor(background)
    blt.clear_area(x, y, width, 1)
    blt.bkcolor(last_bg)

    if bar_width > 0:
        last_bg = blt.state(blt.TK_BKCOLOR)
        blt.bkcolor(foreground)
        blt.clear_area(x, y, bar_width, 1)
        blt.bkcolor(last_bg)

    text = name + ':' + str(value) + '/' + str(max_val)
    x_centered = x + (width - len(text)) // 2
    blt.color('white')
    blt.puts(x_centered, y, text)


def create_window(x, y, w, h, title=None):
    last_bg = blt.state(blt.TK_BKCOLOR)
    blt.bkcolor(blt.color_from_argb(200, 0, 0, 0))
    blt.clear_area(x, y, w + 1, h + 1)
    blt.bkcolor(last_bg)

    border = '[U+250C]' + '[U+2500]'*(w - 2) + '[U+2510]'
    blt.puts(x, y, '[font=small]' + border)
    for i in range(1, h):
        blt.puts(x, y + i, '[font=small][U+2502]')
        blt.puts(x + w - 1, y + i, '[font=small][U+2502]')
    border = '[U+2514]' + '[U+2500]'*(w - 2) + '[U+2518]'
    blt.puts(x, y + h, '[font=small]' + border)

    if title is not None:
        leng = len(title)
        offset = (w + 2 - leng) // 2
        blt.clear_area(x + offset, y, leng, 1)
        blt.puts(x + offset, y, '[font=small]' + title)


def get_names_under_mouse(mouse, fov_cells, camera, dic):
    x = mouse[0]  # - 1
    y = mouse[1]  # - 1
    # print(x, y)
    (map_x, map_y) = camera.to_map_coordinates(x, y)
    # print("Map coords ", map_x, map_y)
    # names = [dic.get((map_x, map_y)).name for (map_x, map_y) in dic
    #          if ((map_x, map_y) in dic and (map_x, map_y) in fov_cells)]
    names = ''
    if (map_x, map_y) in dic:
        # print("target in dic")
        if (map_x, map_y) in fov_cells:
            # print("target in fov")
            names = []
            names.append(dic.get((map_x, map_y)).name)
            # print(names)
            names = ', '.join(names)
            # print(names)

    return names.capitalize()


def render_all(game_map, camera, player, mouse,
               entities, items, corpses, fov_cells):
    terrain = game_map.terrain
    water = game_map.water
    camera.move_camera(player.x, player.y, game_map)
    # print('Camera x: ' + str(camera.x))
    # print('Camera y: ' + str(camera.y))
    # start = time.time()
    decor = get_names_under_mouse(mouse, fov_cells, camera, terrain)
    creatures = get_names_under_mouse(mouse, fov_cells, camera, entities)
    itms = get_names_under_mouse(mouse, fov_cells, camera, items)
    remains = get_names_under_mouse(mouse, fov_cells, camera, corpses)
    layers = []
    if creatures:
        layers.append(creatures)
    if itms:
        layers.append(itms)
    if remains:
        layers.append(remains)
    if decor:
        layers.append(decor)
    screen_width = blt.state(blt.TK_WIDTH)
    screen_height = blt.state(blt.TK_HEIGHT)
    sidebar_width = screen_width - camera.width - 2
    sidebar_x = camera.width + 2
    panel_height = screen_height - camera.height - 3
    panel_y = camera.height + 2

    create_window(0, 0, camera.width + 2, camera.height + 1)
    create_window(0, panel_y, camera.width + 2,
                  panel_height, 'MESSAGE LOG')
    create_window(sidebar_x, 0, sidebar_width, screen_height - 1,
                  'PLAYER STATS')
    render_bar(sidebar_x + 1, 1, sidebar_width - 2, 'HP', player.fighter.hp,
               player.fighter.max_hp,
               'dark red', 'darkest red')
    # print(items)
    for x in range(1, camera.width):
        for y in range(1, camera.height):
            map_x, map_y = camera.to_map_coordinates(x, y)
            if (map_x, map_y) in fov_cells:
                if (map_x, map_y) in water:
                    render_obj((map_x, map_y), water, camera, 'blue')
                    water.get((map_x, map_y)).explored = True
                elif (map_x, map_y) in terrain:
                    render_obj((map_x, map_y), terrain, camera, 'gray')
                    terrain.get((map_x, map_y)).explored = True
                else:
                    blt.puts(x, y, '[color=dark yellow][U+4055]')

                if (map_x, map_y) in corpses:
                    obj = corpses.get((map_x, map_y))
                    render_obj((map_x, map_y), corpses, camera, obj.color)

                if (map_x, map_y) in items:
                    print("found item", map_x, map_y)
                    obj = items.get((map_x, map_y))
                    render_obj((map_x, map_y), items, camera, obj.color)

                if (map_x, map_y) in entities:
                    obj = entities.get((map_x, map_y))
                    # blt.puts(x, y, '[color=yellow][U+2146]')
                    render_obj((map_x, map_y), entities, camera, obj.color)
            elif ((map_x, map_y) in terrain and
                  terrain.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), terrain, camera, 'darker orange')
            elif ((map_x, map_y) in water and
                  water.get((map_x, map_y)).explored):
                render_obj((map_x, map_y), water, camera, 'darker blue')


    names = ''
    for i in layers:
        if i == layers[0]:
            names = i
        elif i:
            names = names + ', ' + i

    blt.clear_area(mouse[0] + 1, mouse[1], len(names), 1)
    blt.puts(mouse[0] + 1, mouse[1], names)


def render_obj(coords, dic, camera, color):
    cam_x, cam_y = camera.to_camera_coordinates(coords[0], coords[1])
    map_x, map_y = coords
    blt.color(color)
    blt.puts(cam_x, cam_y, dic.get((map_x, map_y)).char)
    blt.color('white')
