import subprocess
from pathlib import Path
from typing import Any
from PIL import Image


class ImagePixelIter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class ImageUtils:
    def __init__(self, image: str|None = None):
        if image:
            self.image = Image.open(image)
        self.raster = None


    def iter(self):
        if not self.image:
            return
        
        if not self.raster:
            self.raster: Any = self.image.load()

        for x in range(self.image.width):
            for y in range(self.image.height):
                yield ImagePixelIter(x, y, self.raster[x, y])


    @staticmethod
    def animation(frames: list[Image.Image], path: str, frame_duration: int = 250):
        converted_frames: list[Image.Image] = [f.convert("P") for f in frames]
        converted_frames[0].save(path, save_all=True, append_images=converted_frames[1:], duration=frame_duration, loop=0)


    @staticmethod
    def video(frames: list[Image.Image], out_path: str, fps: int = 60):
        frames_dir = Path(out_path).with_suffix("").parent / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        # for i, f in enumerate(frames):
        #     f.convert("RGB").save(frames_dir / f"frame_{i:06d}.png")

        # Run ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", str(frames_dir / "frame_%06d.png"),
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            out_path
        ]
        subprocess.run(cmd, check=True)

        return out_path
