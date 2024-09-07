import base64
import io
import random
from PIL import Image
import re


rgba_pattern = re.compile(
    r'^((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
    r'((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
    r'((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
    r'((?:0(\.\d*)?|1(\.0*)?)|(?:0?\.\d+))$'
)
hsl_regex = re.compile(r'(\d{1,3}),(\d{1,3}),(\d{1,3})')


def generate_rgba_from_hex(hex_code: str) -> tuple[int, int, int, int]:
    if len(hex_code) == 6:
        hex_code = hex_code + "FF"

    if len(hex_code) == 8:
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        a = int(hex_code[6:8], 16)
        return r, g, b, a

    raise ValueError(hex_code)


def generate_image_from_rgba(rgba: tuple[int, int, int, int], size: int, fav: bool):
    image_tamanho = (size, size)
    image = Image.new("RGBA", image_tamanho, rgba)
    image_io = io.BytesIO()
    image.save(image_io, format="PNG", optimize=True, quality=10)
    if not fav:
        image_base64 = base64.b64encode(image_io.getvalue()).decode("utf-8")
        return image_base64
    image_io.seek(0)
    return image_io


def generate_random_hex():
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


def generate_rgba_from_rgb(rgb_code: str):
    if len(rgb_code.split(',')) > 3:
        raise ValueError(rgb_code)
    r, g, b = map(int, rgb_code.split(','))
    return r, g, b, 255


def generate_rgba_from_rgba(rgba_code: str):
    if not rgba_pattern.match(rgba_code):
        raise ValueError(f"Invalid RGBA format or values out of range: {rgba_code}")

    r, g, b, a = map(float, rgba_code.split(','))
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 1):
        raise ValueError(f"RGBA values out of range: {rgba_code}")

    return int(r), int(g), int(b), int(round(a * 255))


def hsl_to_rgb(h, s, l): # NOQA
    s /= 100
    l /= 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    r = (r + m) * 255 # NOQA
    g = (g + m) * 255 # NOQA
    b = (b + m) * 255 # NOQA

    return round(r), round(g), round(b)


def generate_rgba_from_hsl(hsl_code: str):
    match = hsl_regex.match(hsl_code)
    if not match:
        raise ValueError(f"Invalid HSL format: {hsl_code}")
    h, s, l = map(int, match.groups()) # NOQA
    if not (0 <= h <= 360):
        raise ValueError(f"Hue value out of range: {h}")
    if not (0 <= s <= 100):
        raise ValueError(f"Saturation value out of range: {s}")
    if not (0 <= l <= 100):
        raise ValueError(f"Lightness value out of range: {l}")

    h, s, l = map(int, match.groups()) # NOQA
    r, g, b = hsl_to_rgb(h, s, l)
    return int(r), int(g), int(b), 255


def rgba_to_hex(rgba):
    if len(rgba) != 4:
        raise ValueError("The tuple must have exactly 4 elements: (R, G, B, A).")

    r, g, b, a = rgba
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 255):
        raise ValueError("The values of R, G, B and A must be between 0 and 255.")
    rgb_hex = f'{r:02X}{g:02X}{b:02X}'
    a_hex = f'{a:02X}'
    return rgb_hex + a_hex















