from random import randrange, random
from image_helpers import ImageUtils
from simulation import Simulation
from boid import Boid

FPS = 60
SECONDS = 60
BOIDS = 69
BOID_SPEED = 25
SCALE = 4
GRID_SIZE = 10
SIZE = 153

frames = []

sim = Simulation(SIZE, SIZE, (1.0 / FPS))
sim.boids = [Boid(randrange(0, SIZE - 1), randrange(0, SIZE - 1), 1, sim) for _ in range(BOIDS)]

for boid in sim.boids:
    boid.direction = Boid.deg2vec(randrange(0, 360))
    boid.interpolated_dir = boid.direction
    # boid.speed = (BOID_SPEED + 10 * random()) * (1.0 / FPS)
    boid.speed = BOID_SPEED * (1.0 / FPS)

for i in range(FPS * SECONDS):
    sim.step()
    frames.append(sim.draw(SCALE))

print(f"Rendering {len(frames)} frames...")

# ImageUtils.animation(images, "./output.gif", round(1000 / FPS))
ImageUtils.video(frames, "output/output.mp4", FPS)
