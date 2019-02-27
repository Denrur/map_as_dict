from entity import Entity
from fighter import Fighter
from ai import BasicMonster, ConfusedMonster
from random_utils import random_choice_from_dict
from random import randint


def place_entities(x, y, size, entities, items, game_map,
                   max_monsters_per_room,
                   max_items_per_room):
    number_of_monsters = randint(10, max_monsters_per_room)
    number_of_items = randint(10, max_items_per_room)
    # print("Monsters ", number_of_monsters)
    # print("Items ", number_of_items)
    monster_chances = {'ghost': 80, 'angry_ghost': 20}
    item_chances = {'heal potion': 70, 'lightning scroll': 10,
                    'fireball scroll': 10, 'confuse scroll': 10}
    print("coords ", x, y)
    for i in range(number_of_monsters):
        mx = randint(x, x + size)
        my = randint(y, y + size)
        print("monsters coord ", mx, my)
        if (not (mx, my) in entities) and (not (mx, my) in game_map.terrain):
            monster_choice = random_choice_from_dict(monster_chances)

            if monster_choice == 'ghost':
                fighter_component = Fighter(hp=1, defense=0, power=1)
                ai_component = BasicMonster()
                monster = Entity(mx, my, '[U+7030]', 'gray', 'Ghost',
                                 fighter=fighter_component,
                                 ai=ai_component)
            else:
                fighter_component = Fighter(hp=1, defense=1, power=1)
                ai_component = BasicMonster()
                monster = Entity(mx, my, '[U+7010]', 'white', 'Troll',
                                 fighter=fighter_component,
                                 ai=ai_component)
            entities[(monster.x, monster.y)] = monster
    for i in range(number_of_items):
        print('Items start pont', x, y)
        ix = randint(x, x + size)
        iy = randint(y, y + size)
        print("items coord", ix, iy)
        if not ((ix, iy) in game_map.terrain) and not ((ix, iy) in items):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'heal potion':
                item = Entity(ix, iy, '[U+3000]', 'red', item_choice)
            elif item_choice == 'lightning scroll':
                item = Entity(ix, iy, '[U+6000]', 'yellow', item_choice)
            elif item_choice == 'fireball scroll':
                item = Entity(ix, iy, '[U+6000]', 'red', item_choice)
            elif item_choice == 'confuse scroll':
                item = Entity(ix, iy, '[U+6000]', 'pink', item_choice)

            items[(item.x, item.y)] = item
