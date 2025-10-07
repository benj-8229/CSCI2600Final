from typing import Any
from PIL import Image

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
    min_c = v - s * v
    f = (max_c - min_c) / 60

    if h < 60:   return (max_c, (h - 0) * f + min_c, min_c)
    if h < 120:  return ((120 - h) * f + min_c, max_c, min_c)
    if h < 180:  return (min_c, max_c, (h - 120) * f + min_c)
    if h < 240:  return (min_c, (240 - h) * f + min_c, max_c)
    if h < 300:  return ((h - 240) * f + min_c, min_c, max_c)
    if h < 360:  return (max_c, min_c, (360 - h) * f + min_c)

    return (0, 0, 0)

