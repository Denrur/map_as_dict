import math


class Entity():
    def __init__(self, x, y, char, color, name,
                 blocks=False, block_sight=None, explored=False,
                 fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

        if block_sight is None:
            block_sight = blocks

        self.block_sight = block_sight
        self.explored = explored
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entites):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        x = self.x + dx
        y = self.y + dy
        if (not (x, y) in entites) and (not (x, y) in game_map.terrain):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
