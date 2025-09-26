import math
from random import random

FLOCK_DISTANCE = 15
AVOIDANCE_DISTANCE = 4


class Boid:
    def __init__(self, x_pos: int, y_pos: int, speed: float, sim: 'Simulation'):
        self.x_pos: int = x_pos
        self.y_pos: int = y_pos
        self.speed: float = speed
        self.sim: 'Simulation' = sim
        self.direction: tuple = (0, 0)
        self.interpolated_dir: tuple = (0, 0)

    def move(self):
        self.interpolated_dir = self.lerp_vec(self.interpolated_dir, self.direction, 5 * self.sim.delta)
        self.interpolated_dir = self.normalize_vec(self.interpolated_dir)

        # self.x_pos += self.interpolated_dir[0] * self.speed
        # self.y_pos += self.interpolated_dir[1] * self.speed
        self.x_pos += self.direction[0] * self.speed
        self.y_pos += self.direction[1] * self.speed

    def rotate(self, deg: float = 0):
        current_dir: float = Boid.vec2deg(self.direction)
        new_dir: tuple = Boid.deg2vec(current_dir + deg)
        self.direction = self.normalize_vec(new_dir)

    def steer(self, snapshot: list['Boid']):
        others: list['Boid'] = self.sim.boids_around_boid(snapshot, self, FLOCK_DISTANCE)
        others_close: list['Boid'] = self.sim.boids_around_boid(snapshot, self, AVOIDANCE_DISTANCE)

        aw = .8
        cw = .8
        sw = 1

        ax, ay = self.alignment(others)
        cx, cy = self.cohesion(others)
        sx, sy = self.separation(others_close)

        fx = ax * aw + cx * cw + sx * sw
        fy = ay * aw + cy * cw + sy * sw

        self.direction = self.normalize_vec((fx, fy))

    def alignment(self, others: list['Boid']) -> tuple[float, float]:
        if not others:
            return (0, 0)

        nx, ny = 0, 0

        for other in others:
            dist = self.sim.dist_between_boids(self, other)
            t = dist / FLOCK_DISTANCE
            magnitude = (1 - t) ** 2

            nx += other.interpolated_dir[0] * magnitude
            ny += other.interpolated_dir[1] * magnitude

        return (nx, ny)

    def cohesion(self, others: list['Boid']) -> tuple[float, float]:
        if not others:
            return (0, 0)

        ax = sum(b.x_pos for b in others) / len(others)
        ay = sum(b.y_pos for b in others) / len(others)
        dx = ax - self.x_pos
        dy = ay - self.y_pos
        
        dist = math.sqrt(dx**2 + dy**2)

        nx, ny = dx / dist, dy / dist

        magnitude = min(dist/FLOCK_DISTANCE, 1.0)
        
        return (nx * magnitude, ny * magnitude)

    def separation(self, others: list['Boid']) -> tuple[float, float]:
        if len(others) == 0:
            return (0, 0)

        nx, ny = 0, 0

        for other in others:
            dist = self.sim.dist_between_boids(self, other)
            t = dist / AVOIDANCE_DISTANCE

            if dist < AVOIDANCE_DISTANCE:
                # linear
                # magnitude = 1 - t
                # exponentioanl
                magnitude = (1.0 - t) ** 2
                
                nx += -self.sim.dx_between_boids(self, other) * magnitude
                ny += -self.sim.dy_between_boids(self, other) * magnitude

        return (nx, ny)

    @staticmethod 
    def deg2vec(deg: float) -> tuple:
        rad = math.radians(deg)
        return (math.cos(rad), math.sin(rad))

    @staticmethod
    def vec2deg(vec: tuple[float, float]) -> float:
        return math.degrees(math.atan2(vec[1], vec[0]))

    @staticmethod
    def normalize_vec(vec: tuple[float, float]) -> tuple[float, float]:
        magnitude = math.sqrt(vec[0] ** 2 + vec[1] ** 2)

        # random direction when magnitude is 0 to introduce chaos
        if magnitude == 0:
            return Boid.deg2vec(random() * 360)

        out = (vec[0] / magnitude, vec[1] / magnitude)
        return out

    @staticmethod
    def lerp_vec(a, b, t) -> tuple[float, float]:
        ax, ay = a
        bx, by = b
        cx = ax + (bx - ax) * t
        cy = ay + (by - ay) * t

        return (cx, cy)
