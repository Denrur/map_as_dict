# import numpy as np
# from opensimplex import OpenSimplex
import noise
# import random
import matplotlib.pyplot as plt


class NoiseMap:
    def __init__(self, width=256, height=256,
                 scale=200, octaves=5,
                 persistance=0.3, lactunarity=1.25):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistance = persistance
        self.lactunarity = lactunarity
        self.heightMap = self.GenerateNoiseMap()

    def GenerateNoiseMap(self):
        noise_map = dict()

        max_noise_height = float('-inf')
        min_noise_height = float('inf')

        for y in range(self.height):
            for x in range(self.width):
                noise_value = noise.snoise2(x/self.scale,
                                            y/self.scale,
                                            self.octaves,
                                            self.persistance,
                                            self.lactunarity)
                if noise_value > max_noise_height:
                    max_noise_height = noise_value
                elif noise_value < min_noise_height:
                    min_noise_height = noise_value
                noise_map[(x, y)] = noise_value

        return noise_map


if __name__ == '__main__':
    data = NoiseMap()
    plt.imshow(data.heightMap, cmap='gray', interpolation='nearest')
    plt.show()
