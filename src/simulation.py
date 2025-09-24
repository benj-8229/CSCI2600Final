from typing import Any
from PIL import Image
from boid import Boid

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
        
        for boid in self.boids:
            clampX, clampY = self.mapX(boid.x_pos), self.mapY(boid.y_pos)
            boid.x_pos = clampX
            boid.y_pos = clampY

    def mapX(self, x):
        if self.wrapping:
            x = x % self.x_size
        else:
            x = max(0, min(x, self.x_size - 1))
        return x

    def mapY(self, y):
        if self.wrapping:
            y = y % self.y_size
        else:
            y = max(0, min(y, self.y_size - 1))
        return y

    def draw(self, scale: int = 1) -> Image.Image:
        grid = self.grid.copy()
        raster: Any = grid.load()

        for boid in self.boids:
            # draw boid as white
            raster[int(boid.x_pos), int(boid.y_pos)] = (255, 255, 255)

            # draw boid heading as red
            headX = self.mapX(int(boid.x_pos + boid.direction[0]))
            headY = self.mapY(int(boid.y_pos + boid.direction[1]))
            raster[headX, headY] = (255, 0, 0)

        return grid.resize((self.x_size * scale, self.y_size * scale), Image.NEAREST)
