from noise_map import NoiseMap
# import numpy as np
import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pdb
from entity import Entity
from tabulate import tabulate


class Terrain_generator:
    def __init__(self, width, height,
                 scale, octaves,
                 persistance, lactunarity, game_map):
        self.width = game_map.width
        self.height = game_map.height
        self.scale = scale
        self.octaves = octaves
        self.persistance = persistance
        self.lactunarity = lactunarity
        self.terrain = self.GenearteTerrain(game_map)

    def GenearteTerrain(self, game_map):
        terrain = NoiseMap(width=self.width,
                           height=self.height,
                           scale=self.scale,
                           octaves=self.octaves,
                           persistance=self.persistance,
                           lactunarity=self.lactunarity)
        # print(tabulate(terrain.heightMap))
        for y in range(self.height):
            for x in range(self.width):
                if terrain.heightMap[(x, y)] < -0.3:
                    terrain.heightMap[(x, y)] = -1
                    game_map.water[(x, y)] = Entity(x, y, '~',
                                                    'blue', 'water')
                elif terrain.heightMap[(x, y)] < 0:
                    terrain.heightMap[(x, y)] = -0.3
                elif terrain.heightMap[(x, y)] < 0.5:
                    terrain.heightMap[(x, y)] = 0
                    game_map.terrain[(x, y)] = Entity(x, y, '#',
                                                      'grey', 'wall')
        # print(tabulate(terrain.heightMap))
        return terrain.heightMap


if __name__ == '__main__':
    '''
    while True:
        # pdb.set_trace()
        scale = int(input(" Choose scale from 0 to 500: "))
        if scale == '':
            scale = 200
        octaves = int(input("Choose number of octaves from 1 to 10: "))
        if octaves == '':
            octaves = 5
        persistance = float(input("choose perisitance from 0 to 1 :"))
        if persistance == '':
            persistance = 0.5
        lactunarity = int(input("choose lactunarity from 1 to 10: "))
        if lactunarity == '':
            lactunarity = 1.25

    for s in [100, 200, 300]:
        for o in [2, 4, 6]:
            for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
                for l in [2, 4, 5]:
                    '''
    # pdb.set_trace()
    # cmap = plt.cm.terrain
    # cmaplist = cmap(np.linspace(0, cmap.N, 7))
    # cmap = cmap.from_list("cmap_terrain", cmaplist, cmap.N)

    terra = Terrain_generator(700, 700, 100, 8, 0.5, 2)
    plt.subplot(221)
    plt.imshow(terra.terrain, cmap='terrain')  # plt.cm.get_cmap('terrain', 7))
    plt.colorbar()
    # plt.clim(0, 1)
    plt.savefig('1world.png')
    terra = terra.terrain[0:350, 0:350]
    # Terrain_generator(700, 700, 400, 8, 0.5, 2)
    plt.subplot(222)
    plt.imshow(terra, cmap='terrain')  # plt.cm.get_cmap('terrain', 7))
    plt.savefig('1region.png')
    terra = terra[0:175, 0:175]
    # Terrain_generator(700, 700, 800, 8, 0.5, 2)
    plt.subplot(223)
    plt.imshow(terra, cmap='terrain')  # plt.cm.get_cmap('terrain', 7))
    plt.savefig('1local.png')
    terra = terra[0:87, 0:87]
    # Terrain_generator(700, 700, 1600, 8, 0.5, 2)
    plt.subplot(224)
    plt.imshow(terra, cmap='terrain')  # plt.cm.get_cmap('terrain', 7))
    plt.savefig('1game_map.png')
    print(terra)
    # plt.savefig('s' + str(s) + 'o' + str(o) + 'p' + str(p)
    #                            + 'l' + str(l) + '.png')
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.show()
