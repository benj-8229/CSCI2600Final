import math
import numpy as np
from random import random

FLOCK_DISTANCE = 15
AVOIDANCE_DISTANCE = 4


class Boid:
    def __init__(self, x_pos: int, y_pos: int, speed: float, sim: 'Simulation'):
        self.x_pos: float = float(x_pos)
        self.y_pos: float = float(y_pos)
        self.speed: float = speed
        self.sim: 'Simulation' = sim
        self.direction = np.array([0.0, 0.0], dtype=float)
        self.interpolated_dir = np.array([0.0, 0.0], dtype=float)

    def move(self):
        self.interpolated_dir = self.lerp_vec(self.interpolated_dir, self.direction, 6 * self.sim.delta)
        self.interpolated_dir = self.normalize_vec(self.interpolated_dir)

        self.x_pos += self.interpolated_dir[0] * self.speed
        self.y_pos += self.interpolated_dir[1] * self.speed

    def rotate(self, deg: float = 0):
        current_dir: float = Boid.vec2deg(self.direction)
        new_dir = Boid.deg2vec(current_dir + deg)
        self.direction = self.normalize_vec(new_dir)

    def steer(self, snapshot: list['Boid']):
        others: list['Boid'] = self.sim.boids_around_boid(snapshot, self, FLOCK_DISTANCE)
        others_close: list['Boid'] = self.sim.boids_around_boid(snapshot, self, AVOIDANCE_DISTANCE)

        aw = .9
        cw = .7
        sw = .3

        ax, ay = self.alignment(others)
        cx, cy = self.cohesion(others)
        sx, sy = self.separation(others_close)

        fx = ax * aw + cx * cw + sx * sw
        fy = ay * aw + cy * cw + sy * sw

        if fx*fx + fy*fy < 1e-5:
            return

        self.direction = self.normalize_vec(np.array([fx, fy], dtype=float))

    def alignment(self, others: list['Boid']) -> tuple[float, float]:
        if not others:
            return (0.0, 0.0)

        acc = np.array([0.0, 0.0], dtype=float)
        for other in others:
            dist = self.sim.dist_between_boids(self, other)
            t = dist / FLOCK_DISTANCE
            magnitude = (1.0 - t) ** 2
            acc += np.array(other.interpolated_dir, dtype=float) * magnitude

        return (float(acc[0]), float(acc[1]))

    def cohesion(self, others: list['Boid']) -> tuple[float, float]:
        if not others:
            return (0.0, 0.0)

        if len(others) > 3:
            avg_vel = sum(b.speed for b in others) / len(others)
            self.speed = max(30 * self.sim.delta, self.lerp_float(self.speed, avg_vel, .75 * self.sim.delta))

        # Average position
        ax = sum(b.x_pos for b in others) / len(others)
        ay = sum(b.y_pos for b in others) / len(others)
        d = np.array([ax - self.x_pos, ay - self.y_pos], dtype=float)

        dist = float(np.hypot(d[0], d[1]))
        if dist == 0.0:
            return (0.0, 0.0)

        n = d / dist
        magnitude = min(dist / FLOCK_DISTANCE, 1.0)
        n *= magnitude

        return (float(n[0]), float(n[1]))

    def separation(self, others: list['Boid']) -> tuple[float, float]:
        if len(others) == 0:
            return (0.0, 0.0)

        acc = np.array([0.0, 0.0], dtype=float)
        for other in others:
            dist = self.sim.dist_between_boids(self, other)
            t = dist / AVOIDANCE_DISTANCE
            if dist < AVOIDANCE_DISTANCE:
                magnitude = (1.0 - t) ** 2
                acc += -np.array([self.sim.dx_between_boids(self, other),
                                  self.sim.dy_between_boids(self, other)], dtype=float) * magnitude

        return (float(acc[0]), float(acc[1]))

    @staticmethod
    def deg2vec(deg: float):
        rad = np.radians(deg)
        return np.array([np.cos(rad), np.sin(rad)], dtype=float)

    @staticmethod
    def vec2deg(vec) -> float:
        v = np.asarray(vec, dtype=float)
        return float(np.degrees(np.arctan2(v[1], v[0])))

    @staticmethod
    def normalize_vec(vec):
        v = np.asarray(vec, dtype=float)
        m = float(np.linalg.norm(v))
        if m == 0.0:
            # keep original behavior (random)
            return Boid.deg2vec(random() * 360.0)
        return v / m

    @staticmethod
    def lerp_float(a, b, t) -> float:
        # fix: correct linear interpolation
        return float(a + (b - a) * t)

    @staticmethod
    def lerp_vec(a, b, t):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        return a + (b - a) * t

