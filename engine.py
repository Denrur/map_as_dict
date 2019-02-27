from bearlibterminal import terminal as blt
from camera import Camera
from chunks import add_new_chunks
from death_functions import kill_player, kill_monster
from entity import Entity
from fighter import Fighter
# from fov_functions import recompute_fov
from game_map import GameMap
from render_functions import render_all
from input_handlers import handle_keys
# from terrain_generation import Terrain_generator
# from place_entities import place_entities
# from new_bsp_generator import make_bsp
import time
import rpas
# import numpy


def main():
    print("Start")
    # blt.set("window: size=80x25, cellsize=auto;""input : filter={keyboard}")
    blt.color("white")
    fighter_component = Fighter(hp=30, defense=3, power=5)

    player = Entity(
        27,
        27,
        '[U+1090]',
        'white',
        'player',
        fighter=fighter_component)
    health_potion = Entity(
        25,
        25,
        '[U+7012]',
        'green',
        'healing')
    print("Generating map")
    start = time.time()
    entities = dict()
    items = dict()
    corpses = dict()

    game_map = GameMap(0, 0)

    chunk_size = 50

    max_monsters_per_chunk = 50
    max_items_per_chunk = 30
    cx = player.x // chunk_size * chunk_size
    cy = player.y // chunk_size * chunk_size
    add_new_chunks(cx, cy, chunk_size, game_map, entities, items,
                   max_monsters_per_chunk, max_items_per_chunk)

    # print(game_map.chunks)
    items[(health_potion.x, health_potion.y)] = health_potion
    entities[(player.x, player.y)] = player
    print(time.time() - start)
    print("BPS")
    # start = time.time()
    # make_bsp(game_map, 20, 5, player, entities, items, 3, 1)
    # blt.composition(True)
    camera = Camera(40, 20, 0, 0)
    blt.open()
    # print(time.time() - start)

    def is_unobstruct(x, y):
        if (x, y) in game_map.terrain:
            return False
        else:
            return True
    fov = rpas.FOVCalc()

    while True:
        mouse_x = blt.state(blt.TK_MOUSE_X)
        mouse_y = blt.state(blt.TK_MOUSE_Y)
        mouse = (mouse_x, mouse_y)
        blt.composition(True)
        # set_trace()
        blt.clear()
        # blt.bkcolor('green')
        # start = time.time()
        fov_cells = fov.calc_visible_cells_from(
            player.x, player.y, 20, is_unobstruct)
        # print(fov_cells)
        # recompute_fov(game_map, player.x, player.y, radius=5)
        # print(game_map.fov)
        render_all(game_map, camera, player, mouse,
                   entities, items, corpses,
                   fov_cells)
        # blt.put(2, 1, 0x2000)
        # blt.put(1, 1, 0x1000)
        # print(player.x)
        # print(player.y)
        blt.refresh()
        # print(time.time() - start)
        action = handle_keys()

        move = action.get('move')
        exit = action.get('exit')

        player_turn_results = []
        # print(len(game_map.terrain))
        # print(len(game_map.water))
        if move:
            dx, dy = move
            dest_x = player.x + dx
            dest_y = player.y + dy
            if (dest_x, dest_y) in game_map.terrain:
                continue
            if entities.get((dest_x, dest_y)):
                target = entities.get((dest_x, dest_y))
                attack_results = player.fighter.attack(target)
                player_turn_results.extend(attack_results)
            else:
                entities.pop((player.x, player.y))
                player.move(dx, dy)
                entities[(player.x, player.y)] = player

        if exit:
            return False
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message.text)

            if dead_entity:
                if dead_entity == player:
                    message = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity, entities, corpses)
                print(message.text)
        print("Entites ", len(entities))
        i = 0
        entities_done = set()
        for entity in entities:
            # print(entities[entity])
            if (entities[entity] != player and
                    not (entity in entities_done) and
                    entity in fov_cells):
                enemy = entities.pop(entity)

                enemy.move_towards(player.x, player.y, game_map, entities)
                entities[(enemy.x, enemy.y)] = enemy
                entities_done.add((enemy.x, enemy.y))
                i += 1
        print(i)


        # print("input delay: %s" % (time.time() - start))
        cx = (player.x // chunk_size) * chunk_size
        cy = (player.y // chunk_size) * chunk_size

        add_new_chunks(cx, cy, chunk_size, game_map, entities, items,
                       max_monsters_per_chunk, max_items_per_chunk)
        # print(len(game_map.chunks))
        # print(len(items))


if __name__ == "__main__":
    main()
