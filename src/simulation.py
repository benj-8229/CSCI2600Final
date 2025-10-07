import math
from copy import deepcopy
from typing import Any
from PIL import Image
from boid import Boid
from hsv import hsv_to_rgb

BOID_COLOR = (255, 255, 255)
BOID_HEAD_COLOR = (245, 93, 227)

class Simulation:
    def __init__(self, x_size: int = 350, y_size: int = 350, delta: float = 1 / 60, wrapping: bool = True, grid_size: int = 8):
        self.x_size = x_size
        self.y_size = y_size
        self.delta = delta
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
        # create a snapshot without the circular reference to sim
        snapshot = []
        for boid in self.boids:
            boid.sim = None
            b = deepcopy(boid)
            b.sim = None
            boid.sim = self
            snapshot.append(b)

        for boid in self.boids:
            boid.steer(snapshot)

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

    def boids_around_boid(self, boids: list[Boid], boid: Boid, r: float) -> list[Boid]:
        out = []

        for other in boids:
            d = self.dist_between_boids(boid, other)
            if other != boid and d > 1e-6 and d <= r:
                    out.append(other)

        return out

    def dist_between_boids(self, a: Boid, b: Boid) -> float:
        dx = abs(b.x_pos - a.x_pos)
        dy = abs(b.y_pos - a.y_pos)

        if not self.wrapping:
            return math.sqrt(dx**2 + dy**2)

        if dx > .5 * self.x_size:
            dx -= self.x_size

        if dy > .5 * self.y_size:
            dy -= self.y_size

        return math.sqrt(dx**2 + dy**2)

    def dx_between_boids(self, a: Boid, b: Boid) -> float:
        dx = b.x_pos - a.x_pos
        if not self.wrapping:
            return dx
        # 3) symmetric wrap
        half = 0.5 * self.x_size
        if dx >  half: dx -= self.x_size
        if dx < -half: dx += self.x_size
        return dx

    def dy_between_boids(self, a: Boid, b: Boid) -> float:
        dy = b.y_pos - a.y_pos
        if not self.wrapping:
            return dy
        half = 0.5 * self.y_size
        if dy >  half: dy -= self.y_size
        if dy < -half: dy += self.y_size
        return dy

    def draw(self, scale: int = 1) -> Image.Image:
        grid = self.grid.copy()
        raster: Any = grid.load()

        for boid in self.boids:
            h = (Boid.vec2deg(boid.interpolated_dir) + 360) % 360
            r, g, b = hsv_to_rgb(h, 1, 1)
            BOID_HEAD_COLOR = (int(r * 255), int(g * 255), int(b * 255))
    
            mapX, mapY = self.map_x(round(boid.x_pos)), self.map_y(round(boid.y_pos))
            raster[mapX, mapY] = BOID_COLOR

            # draw boid heading
            headX = self.map_x(round(boid.x_pos + boid.direction[0]))
            headY = self.map_y(round(boid.y_pos + boid.direction[1]))

            raster[headX, headY] = BOID_HEAD_COLOR

        return grid.resize((self.x_size * scale, self.y_size * scale), Image.NEAREST)
