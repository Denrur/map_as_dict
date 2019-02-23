class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.full_rooms = False
        self.water = self.initialize_water()
        self.terrain = self.initialize_terrain()
        self.chunks = set()

    def initialize_terrain(self):
        terrain = dict()
        return terrain

    def initialize_water(self):
        water = dict()
        return water
