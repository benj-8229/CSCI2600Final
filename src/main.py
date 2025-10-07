import subprocess
from pathlib import Path
from random import randrange, random
from simulation import Simulation
from boid import Boid

FPS = 60
SECONDS = 30
BOIDS = 35
BOID_SPEED = 30
SCALE = 4
GRID_SIZE = 10
SIZE = 153
OUTPUT_PATH = "output/output.mp4"

print(f"Calculating {FPS * SECONDS} frames with a delta of {1.0/FPS}")

frames_dir = Path(OUTPUT_PATH).with_suffix("").parent / "frames"
frames_dir.mkdir(parents=True, exist_ok=True)

sim = Simulation(SIZE, SIZE, (1.0 / FPS))
sim.boids = [Boid(randrange(0, SIZE - 1), randrange(0, SIZE - 1), 1, sim) for _ in range(BOIDS)]
for boid in sim.boids:
    boid.direction = Boid.deg2vec(randrange(0, 360))
    boid.interpolated_dir = boid.direction
    boid.speed = (BOID_SPEED + 20 * random()) * (1.0 / FPS)
    #boid.speed = BOID_SPEED * (1.0 / FPS)


for i in range(FPS * SECONDS):
    sim.step()
    frame = sim.draw(SCALE)
    frame.convert("RGB").save(frames_dir / f"frame_{i:06d}.png")


print(f"Rendering {FPS * SECONDS} frames...")
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", str(frames_dir / "frame_%06d.png"),
    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    OUTPUT_PATH
]
subprocess.run(cmd, check=True)
