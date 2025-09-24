import math

class Boid:
    def __init__(self, x_pos: int = 0, y_pos: int = 0, speed: float = 1):
        self.x_pos: int = x_pos
        self.y_pos: int = y_pos
        self.speed: float = speed
        self.direction: tuple = (1, 0)

    def move(self):
        self.x_pos += self.direction[0] * self.speed
        self.y_pos += self.direction[1] * self.speed

    def rotate(self, deg: float = 0):
        current_dir: float = Boid.vec2deg(self.direction)
        new_dir: tuple = Boid.deg2vec(current_dir + deg)
        self.direction = new_dir

    @staticmethod 
    def deg2vec(deg: float) -> tuple:
        return (math.cos(deg), math.sin(deg))

    @staticmethod
    def vec2deg(vec: tuple[float, float]) -> float:
        return math.atan2(vec[1], vec[0]) * (180 / math.pi)
