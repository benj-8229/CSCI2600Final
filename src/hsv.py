from typing import Any
from PIL import Image

image = Image.open('./starry.jpeg')
raster: Any = image.load()
image.show()

# rgb255
def rgb_to_hsv(r, g, b):
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    v = max_c
    if v == 0:
        return 0, 0, 0

    s = delta / max_c
    if s == 0:
        return 0, s, v

    angle_scale = 60 / delta
    if r == max_c:
        h = (360 + (g - b) * angle_scale) % 360
    elif g == max_c:
        h = 120 + (b - r) * angle_scale
    else:
        h = 240 + (r - g) * angle_scale

    return h, s, v

def hsv_to_rgb(h, s, v):
    max_c = v
    min_c = max_c - s*v
    f = (max_c - min_c) / 60

    if h < 60: return (max_c, (h-0) * f + min_c, min_c)
    if h < 120: return (min_c - (h-120), max_c, min_c)
    if h < 180: return (min_c, max_c, (h-120) * f + min_c)
    if h < 240: return (min_c, min_c-(h-240)*f, max_c)
    if h < 300: return ((h-240) * f + min_c, min_c, max_c)
    if h < 360: return (max_c, min_c, min_c-(h-360) * f)

    return (0, 0, 0)

for x in range(image.width):
    for y in range(image.height):
        r, g, b, *_ = raster[x, y]

        h, s, v = rgb_to_hsv(r, g, b)
        r, g, b = hsv_to_rgb(h, 1, v)

        r = int(r)
        g = int(g)
        b = int(b)

        raster[x,y] = r, g, b

image.resize((image.width*2, image.height*2)).show()
