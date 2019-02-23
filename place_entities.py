from entity import Entity
from fighter import Fighter
from ai import BasicMonster
from random_utils import random_choice_from_dict
from random import randint


def place_entities(x, y, size, entities, items, game_map,
                   max_monsters_per_room,
                   max_items_per_room):
    number_of_monsters = randint(0, max_monsters_per_room)
    number_of_items = randint(0, max_items_per_room)

    monster_chances = {'ghost': 80, 'angry_ghost': 20}
    item_chances = {'heal_potion': 70, 'lightning_scroll': 10,
                    'fireball_scroll': 10, 'confuse_scroll': 100}
    for i in range(number_of_monsters):
        x = randint(x, x + size)
        y = randint(y, y + size)

        if (not (x, y) in entities) and (not (x, y) in game_map.terrain):
            monster_choice = random_choice_from_dict(monster_chances)

            if monster_choice == 'ghost':
                fighter_component = Fighter(hp=1, defense=0, power=1)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'g', 'green', 'Ghost',
                                 fighter=fighter_component,
                                 ai=ai_component)
            else:
                fighter_component = Fighter(hp=1, defense=1, power=1)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'G', 'darker green', 'Angry Ghost',
                                 fighter=fighter_component,
                                 ai=ai_component)
            entities[(monster.x, monster.y)] = monster
    for i in range(number_of_items):
        x = randint(x, x + size)
        y = randint(y, y + size)

        if not ((x, y) in game_map.terrain) or not ((x, y) in items):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'heal_potion':
                item = Entity(x, y, '!', 'blue', item_choice)
            elif item_choice == 'lightning_scroll':
                item = Entity(x, y, '#', 'yellow', item_choice)
            elif item_choice == 'fireball_scroll':
                item = Entity(x, y, '#', 'red', item_choice)
            elif item_choice == 'confuse_scroll':
                item = Entity(x, y, '#', 'pink', item_choice)

            items[(item.x, item.y)] = item
