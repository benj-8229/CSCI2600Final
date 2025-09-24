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


    def step(self):
        for boid in self.boids:
            boid.move()
        
        for boid in self.boids:
            if self.wrapping:
                boid.x_pos = boid.x_pos % self.x_size
                boid.y_pos = boid.y_pos % self.y_size
                # self.wrap_boid_position(boid)
            else:
                boid.x_pos = min(boid.x_pos, self.x_size-1) # clamp right border
                boid.x_pos = max(boid.x_pos, 0)             # clamp left border
                boid.y_pos = min(boid.y_pos, self.y_size-1) # clamp bottom border
                boid.y_pos = max(boid.y_pos, 0)             # clamp top border


    def wrap_boid_position(self, boid: Boid):
        if boid.x_pos < 0:
            boid.x_pos += self.x_size
        elif boid.x_pos >= self.x_size:
            boid.x_pos -= self.x_size

        if boid.y_pos < 0:
            boid.y_pos += self.y_size
        elif boid.y_pos >= self.y_size:
            boid.y_pos -= self.y_size


    def draw(self, scale: int = 1) -> Image.Image:
        render = Image.new("RGB", (self.x_size, self.y_size))
        raster: Any = render.load()

        for x in range(0, self.x_size):
            for y in range(0, self.y_size, 8):
                raster[x, y] = (33, 33, 32)
                raster[y, x] = (33, 33, 32)

        for boid in self.boids:
            raster[int(boid.x_pos), int(boid.y_pos)] = (255, 255, 255)

        return render.resize((self.x_size * scale, self.y_size * scale), Image.NEAREST)
