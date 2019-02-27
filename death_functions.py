# from bearlibterminal import terminal as blt
from game_messages import Message
# from game_states import GameStates
# from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = 'red'

    return Message('You died!', 'red')  # , GameStates.PLAYER_DEAD


def kill_monster(monster, entities, corpses):
    if monster.name == 'wall':
        death_message = Message('Wall is destroyed', 'orange')
        monster.char = '_'
        monster.color = 'white'
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'splinters of wall'
    else:
        death_message = Message(
            '{0} is dead!'.format(monster.name.capitalize()),
            'orange')

        monster.char = '[U+8028]'
        monster.color = 'red'
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        entities.pop((monster.x, monster.y))
        corpses[(monster.x, monster.y)] = monster
        # print(corpses)

    return death_message
