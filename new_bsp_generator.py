from rectangle import Room
# from random import choice
# import functools
import tcod.bsp
from entity import Entity
from fighter import Fighter
from place_entities import place_entities


def make_bsp(game_map, depth, min_size, player, entities, items,
             max_monsters_per_room, max_items_per_room):
    mmpr = max_monsters_per_room
    mipr = max_items_per_room
    bsp = tcod.bsp.BSP(0, 0, game_map.width, game_map.height)
    bsp.split_recursive(depth, min_size + 1, min_size + 1, 1.5, 1.5)
    for node in bsp.pre_order():
        if node.children:
            node1, node2 = node.children
            center_x_node1 = int((node1.x * 2 + node1.width) / 2)
            center_y_node1 = int((node1.y * 2 + node1.height) / 2)
            center_x_node2 = int((node2.x * 2 + node2.width) / 2)
            center_y_node2 = int((node2.y * 2 + node2.height) / 2)
            maxx = max(center_x_node1, center_x_node2)
            minx = min(center_x_node1, center_x_node2)
            maxy = max(center_y_node1, center_y_node2)
            miny = min(center_y_node1, center_y_node2)
            if center_x_node1 == center_x_node2:
                for y in range(miny, maxy):
                    if (center_x_node1, y) in game_map.terrain:
                        # floor = Entity(center_x_node1, y,
                        #                '.', 'white', 'floor')
                        del game_map.terrain[(center_x_node1, y)]
                        # game_map.terrain[(center_x_node1, y)] = floor
                        # game_map.tcod_map.transparent[
                        # y, center_x_node1] = True
            if center_y_node1 == center_y_node2:
                for x in range(minx, maxx):
                    if (x, center_y_node1) in game_map.terrain:
                        # floor = Entity(x, center_y_node1,
                        #                '.', 'white', 'floor')
                        del game_map.terrain[(x, center_y_node1)]
                        # game_map.terrain[(x, center_y_node1)] = floor
                        # game_map.tcod_map.transparent[
                        # center_y_node1, x] = True
        else:
            new_room = Room(node.x, node.y, node.width - 1, node.height - 1)

            for x in range(node.x, node.x + node.width):
                for y in range(node.y, node.y + node.height):
                    # fight = Fighter(hp=1, defense=0, power=0)
                    game_map.terrain[(node.x, y)] = Entity(node.x, y,
                                                           '#', 'white',
                                                           'wall')
                    game_map.terrain[(node.x + node.width, y)] = Entity(
                        node.x+node.width, y, '#', 'white', 'wall')
                    game_map.terrain[(x, node.y)] = Entity(
                        node.x+node.width, y, '#', 'white', 'wall')
                    game_map.terrain[(x, node.y + node.height)] = Entity(
                        node.x+node.width, y, '#', 'white', 'wall')
            place_entities(new_room, entities, items, mmpr, mipr)

    return game_map


'''
def traverse_node(node, _, game_map, entities, entities_pos,
                  mmpr, mipr, min_size):

    if tcod.bsp_is_leaf(node):
        minx = node.x + 1
        maxx = node.x + node.w - 1
        miny = node.y + 1
        maxy = node.y + node.h - 1
        if maxx == game_map.width - 1:
            maxx -= 1
        if maxy == game_map.height - 1:
            maxy -= 1
        if game_map.full_rooms is False:
            minx = tcod.random_get_int(None, minx,
                                       maxx - min_size + 1)
            miny = tcod.random_get_int(None, miny,
                                       maxy - min_size + 1)
            maxx = tcod.random_get_int(None, minx + min_size - 2,
                                       maxx)
            maxy = tcod.random_get_int(None, miny + min_size - 2,
                                       maxy)

        node.x = minx
        node.y = miny
        node.w = maxx - minx + 1
        node.h = maxy - miny + 1
        new_room = Room(node.x, node.y, node.w, node.h)

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                game_map.terrain.pop((x, y))
        place_entities(new_room, entities, mmpr, mipr)

        rooms.append(new_room)

    else:
        left = tcod.bsp_left(node)
        right = tcod.bsp_right(node)
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y

        if node.horizontal:
            if (left.x + left.w - 1 < right.x or
                    right.x + right.w - 1 < left.x):
                x1 = tcod.random_get_int(None, left.x,
                                         left.x + left.w - 1)
                x2 = tcod.random_get_int(None,
                                         right.x,
                                         right.x + right.w - 1)
                y = tcod.random_get_int(None, left.y + left.h, right.y)
                vline_up(game_map, x1, y - 1)
                hline(game_map, x1, y, x2)
                vline_down(game_map, x2, y + 1)
            else:
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = tcod.random_get_int(None, minx, maxx)

                while x > game_map.width - 1:
                    x -= 1
                vline_down(game_map, x, right.y)
                vline_up(game_map, x, right.y - 1)

        else:
            if (left.y + left.h - 1 < right.y or
                    right.y + right.h - 1 < left.y):
                y1 = tcod.random_get_int(None, left.y,
                                         left.y + left.h - 1)
                y2 = tcod.random_get_int(None, right.y,
                                         right.y + right.h - 1)
                x = tcod.random_get_int(None, left.x + left.w, right.x)
                hline_left(game_map, x - 1, y1)
                vline(game_map, x, y1, y2)
                hline_right(game_map, x + 1, y2)
            else:
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = tcod.random_get_int(None, miny, maxy)

                while y > game_map.height - 1:
                    y -= 1

                hline_left(game_map, right.x - 1, y)
                hline_right(game_map, right.x, y)

    return True


def vline(game_map, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        game_map.terrain.remove((x, y))


def vline_up(game_map, x, y):
    while y >= 0 and (x, y) in game_map.terrain:
        game_map.terrain.remove((x, y))
        y -= 1


def vline_down(game_map, x, y):
    while y < game_map.height and (x, y) in game_map.terrain:
        game_map.terrain.remove((x, y))
        y += 1


def hline(game_map, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        game_map.terrain.remove((x, y))


def hline_left(game_map, x, y):
    while x >= 0 and (x, y) in game_map.terrain:
        game_map.terrain.remove((x, y))
        x -= 1


def hline_right(game_map, x, y):
    while x < game_map.width and (x, y) in game_map.terrain:
        game_map.terrain.remove((x, y))
        x += 1
'''
