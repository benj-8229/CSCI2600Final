import noise
import numpy as np


def perlin(offset_x, offset_y, width, height, scale=.03, octaves=6, persistence=.5, lacunarity=2.0, seed=0):
    world = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            world[y][x] = noise.pnoise2(
                (x + offset_x) * scale,
                (y + offset_y) * scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=width, # For seamless tiling if desired
                repeaty=height,
                base=seed)

    world = (world + 1.0) / 2.0
    return world
