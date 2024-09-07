import base64
import io
import random
import re

from PIL import Image

rgba_pattern = re.compile(r'^((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
                          r'((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
                          r'((?:0|[1-9][0-9]?)|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5])),'
                          r'((?:0(\.\d*)?|1(\.0*)?)|(?:0?\.\d+))$'
)
hsl_regex = re.compile(r'(\d{1,3}),(\d{1,3}),(\d{1,3})')
hsla_regex = re.compile(r'^(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(0?\.\d+|1\.0|1)$')
cmyk_regex = re.compile(r'^(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})$')

xyz_regex = re.compile(r'^(\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)$')


def rgba_to_hex(rgba):
    if len(rgba) != 4:
        raise ValueError("The tuple must have exactly 4 elements: (R, G, B, A).")

    r, g, b, a = rgba
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0 <= a <= 255):
        raise ValueError("The values of R, G, B and A must be between 0 and 255.")
    rgb_hex = f'{r:02X}{g:02X}{b:02X}'
    a_hex = f'{a:02X}'
    return rgb_hex + a_hex


def generate_random_hex():
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


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


def hsl_to_rgb(h, s, l):  # NOQA
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
    r = (r + m) * 255  # NOQA
    g = (g + m) * 255  # NOQA
    b = (b + m) * 255  # NOQA

    return round(r), round(g), round(b)


def generate_rgba_from_hsl(hsl_code: str):
    match = hsl_regex.match(hsl_code)
    if not match:
        raise ValueError(f"Invalid HSL format: {hsl_code}")
    h, s, l = map(int, match.groups())  # NOQA
    if not (0 <= h <= 360):
        raise ValueError(f"Hue value out of range: {h}")
    if not (0 <= s <= 100):
        raise ValueError(f"Saturation value out of range: {s}")
    if not (0 <= l <= 100):
        raise ValueError(f"Lightness value out of range: {l}")

    r, g, b = hsl_to_rgb(h, s, l)
    return int(r), int(g), int(b), 255


def generate_rgba_from_hsla(hsla_code: str):
    match = hsla_regex.match(hsla_code)
    if not match:
        raise ValueError(f"Invalid HSL format: {hsla_code}")
    h, s, l, a = map(float, match.groups())  # NOQA
    if not (0 <= h <= 360):
        raise ValueError(f"Hue value out of range: {h}")
    if not (0 <= s <= 100):
        raise ValueError(f"Saturation value out of range: {s}")
    if not (0 <= l <= 100):
        raise ValueError(f"Lightness value out of range: {l}")
    if not (0 <= a <= 1):
        raise ValueError(f"Alpha value out of range: {a}")

    r, g, b = hsl_to_rgb(h, s, l)
    return int(r), int(g), int(b), int(a * 255)


def generate_rgba_from_cmyk(cmyk_code: str):
    match = cmyk_regex.match(cmyk_code)
    if not match:
        raise ValueError(f"Invalid CMYK format: {cmyk_code}")
    c, m, y, k = map(float, match.groups())
    if not (0 <= c <= 100):
        raise ValueError(f"Cyan value out of range: {c}")
    if not (0 <= m <= 100):
        raise ValueError(f"Magenta value out of range: {m}")
    if not (0 <= y <= 100):
        raise ValueError(f"Yellow value out of range: {y}")
    if not (0 <= k <= 100):
        raise ValueError(f"Black value out of range: {k}")

    k = k / 100
    r = 1 - min(1, c / 100 * (1 - k) + k)
    g = 1 - min(1, m / 100 * (1 - k) + k)
    b = 1 - min(1, y / 100 * (1 - k) + k)

    return int(r * 255), int(g * 255), int(b * 255), 255
