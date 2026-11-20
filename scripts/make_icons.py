#!/usr/bin/env python3
"""Draw the app icons: a sun behind a cloud on a near-black tile.

Rendered at 4x and box-filtered down, because PIL is not available and hand-rolled
shapes look jagged without supersampling. Stdlib only.

    python3 scripts/make_icons.py
"""
import math
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALE = 4
BACKGROUND = (14, 14, 14)
SUN = (255, 176, 32)
CLOUD = (215, 222, 232)


def in_circle(x, y, cx, cy, r):
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def in_capsule(x, y, x1, y1, x2, y2, r):
    dx, dy = x2 - x1, y2 - y1
    length = dx * dx + dy * dy
    if length == 0:
        return in_circle(x, y, x1, y1, r)
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / length))
    px, py = x1 + t * dx, y1 + t * dy
    return (x - px) ** 2 + (y - py) ** 2 <= r * r


def in_box(x, y, x0, y0, x1, y1, r):
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    cx = min(max(x, x0 + r), x1 - r)
    cy = min(max(y, y0 + r), y1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def colour_at(x, y, unit):
    """Coordinates are in a 64-unit design space."""
    # cloud first: it sits in front of the sun
    if (in_circle(x, y, 26 * unit, 38 * unit, 10.5 * unit) or
            in_circle(x, y, 42 * unit, 33 * unit, 12.5 * unit) or
            in_box(x, y, 20 * unit, 37 * unit, 50 * unit, 49 * unit, 6 * unit)):
        return CLOUD
    if in_circle(x, y, 24 * unit, 23 * unit, 9.5 * unit):
        return SUN
    for index in range(8):
        angle = index * math.pi / 4
        x1 = 24 * unit + math.cos(angle) * 13 * unit
        y1 = 23 * unit + math.sin(angle) * 13 * unit
        x2 = 24 * unit + math.cos(angle) * 17.5 * unit
        y2 = 23 * unit + math.sin(angle) * 17.5 * unit
        if in_capsule(x, y, x1, y1, x2, y2, 1.9 * unit):
            return SUN
    return BACKGROUND


def chunks(tag, data):
    return (struct.pack(">I", len(data)) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))


def render(size):
    big = size * SCALE
    unit = big / 64.0
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            r = g = b = 0
            for sy in range(SCALE):
                for sx in range(SCALE):
                    cr, cg, cb = colour_at((x * SCALE + sx + 0.5),
                                           (y * SCALE + sy + 0.5), unit)
                    r += cr
                    g += cg
                    b += cb
            n = SCALE * SCALE
            row += bytes((r // n, g // n, b // n))
        rows.append(bytes(row))

    raw = b"".join(rows)
    return (b"\x89PNG\r\n\x1a\n"
            + chunks(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunks(b"IDAT", zlib.compress(raw, 9))
            + chunks(b"IEND", b""))


def main():
    for name, size in (("icon.png", 76), ("icon-152.png", 152), ("icon-192.png", 192),
                       ("favicon.png", 32), ("icon-512.png", 512)):
        path = os.path.join(ROOT, name)
        with open(path, "wb") as handle:
            handle.write(render(size))
        print("%-14s %3dpx %6d B" % (name, size, os.path.getsize(path)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
