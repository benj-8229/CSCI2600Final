import math
from typing import Any
from PIL import Image
from boid import Boid

BOID_COLOR = (255, 255, 255)
BOID_HEAD_COLOR = (245, 93, 227)

class Simulation:
    def __init__(self, x_size: int = 350, y_size: int = 350, wrapping: bool = True, grid_size: int = 8):
        self.x_size = x_size
        self.y_size = y_size
        self.wrapping = wrapping
        self.grid_size = grid_size
        self.boids: list[Boid] = []

        # draw grid
        self.grid = Image.new("RGB", (self.x_size, self.y_size))
        raster: Any = self.grid.load()
        for x in range(0, self.x_size):
            for y in range(0, self.y_size, 8):
                raster[x, y] = (33, 33, 32)
                raster[y, x] = (33, 33, 32)

    def step(self):
        for boid in self.boids:
            boid.move()

    def map_x(self, x):
        if self.wrapping:
            x = x % self.x_size
        else:
            x = max(0, min(x, self.x_size - 1))
        return x

    def map_y(self, y):
        if self.wrapping:
            y = y % self.y_size
        else:
            y = max(0, min(y, self.y_size - 1))
        return y

    def dist_between_boids(self, a: Boid, b: Boid) -> float:
        if self.wrapping:
            pass

        a_pos = [a.x_pos, a.y_pos]
        b_pos = [b.x_pos, b.y_pos]
        return math.dist(a_pos, b_pos)

    def draw(self, scale: int = 1) -> Image.Image:
        grid = self.grid.copy()
        raster: Any = grid.load()

        for boid in self.boids:
            mapX, mapY = self.map_x(round(boid.x_pos)), self.map_y(round(boid.y_pos))
            raster[mapX, mapY] = BOID_COLOR

            # draw boid heading
            headX = self.map_x(round(boid.x_pos + boid.direction[0]))
            headY = self.map_y(round(boid.y_pos + boid.direction[1]))

            raster[headX, headY] = BOID_HEAD_COLOR

        return grid.resize((self.x_size * scale, self.y_size * scale), Image.NEAREST)
