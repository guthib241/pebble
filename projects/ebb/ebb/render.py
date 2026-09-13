"""Raster drawing for the demos: an indexed-colour canvas, discs, and a tiny font.

Stdlib only. Pixels are palette indices in a flat bytearray, which is what
:mod:`ebb.gif` wants.
"""

GLYPHS = {
    "A": "111 101 111 101 101", "B": "110 101 110 101 110", "C": "111 100 100 100 111",
    "D": "110 101 101 101 110", "E": "111 100 111 100 111", "F": "111 100 111 100 100",
    "G": "111 100 101 101 111", "H": "101 101 111 101 101", "I": "111 010 010 010 111",
    "J": "001 001 001 101 111", "K": "101 101 110 101 101", "L": "100 100 100 100 111",
    "M": "101 111 111 101 101", "N": "110 101 101 101 101", "O": "111 101 101 101 111",
    "P": "111 101 111 100 100", "Q": "111 101 101 111 001", "R": "111 101 110 101 101",
    "S": "111 100 111 001 111", "T": "111 010 010 010 010", "U": "101 101 101 101 111",
    "V": "101 101 101 101 010", "W": "101 101 111 111 101", "X": "101 101 010 101 101",
    "Y": "101 101 010 010 010", "Z": "111 001 010 100 111",
    "0": "111 101 101 101 111", "1": "010 110 010 010 111", "2": "111 001 111 100 111",
    "3": "111 001 111 001 111", "4": "101 101 111 001 001", "5": "111 100 111 001 111",
    "6": "111 100 111 101 111", "7": "111 001 001 001 001", "8": "111 101 111 101 111",
    "9": "111 101 111 001 111",
    " ": "000 000 000 000 000", ":": "000 010 000 010 000", "-": "000 000 111 000 000",
    ".": "000 000 000 000 010", ",": "000 000 000 010 010", "/": "001 001 010 100 100",
    "=": "000 111 000 111 000", "!": "010 010 010 000 010", "?": "111 001 010 000 010",
    "<": "001 010 100 010 001", ">": "100 010 001 010 100", "+": "000 010 111 010 000",
    "(": "010 100 100 100 010", ")": "010 001 001 001 010", "'": "010 010 000 000 000",
}


class Canvas:
    def __init__(self, width, height, bg=0):
        self.w = width
        self.h = height
        self.px = bytearray([bg]) * (width * height)

    def fill(self, colour):
        self.px = bytearray([colour]) * (self.w * self.h)

    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = colour

    def hspan(self, x0, x1, y, colour):
        if not (0 <= y < self.h):
            return
        x0 = max(0, x0)
        x1 = min(self.w - 1, x1)
        if x1 < x0:
            return
        row = y * self.w
        self.px[row + x0 : row + x1 + 1] = bytes([colour]) * (x1 - x0 + 1)

    def rect(self, x0, y0, x1, y1, colour):
        for y in range(y0, y1 + 1):
            self.hspan(x0, x1, y, colour)

    def frame(self, x0, y0, x1, y1, colour):
        self.hspan(x0, x1, y0, colour)
        self.hspan(x0, x1, y1, colour)
        for y in range(y0, y1 + 1):
            self.set(x0, y, colour)
            self.set(x1, y, colour)

    def disc(self, cx, cy, r, colour):
        if r <= 0:
            self.set(cx, cy, colour)
            return
        rr = r * r
        for dy in range(-r, r + 1):
            span = int((rr - dy * dy) ** 0.5)
            self.hspan(cx - span, cx + span, cy + dy, colour)

    def line(self, x0, y0, x1, y1, colour):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, colour)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def ring(self, cx, cy, r, colour):
        steps = max(8, 6 * r)
        import math

        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.set(cx + int(round(r * math.cos(a))), cy + int(round(r * math.sin(a))), colour)

    def text(self, x, y, s, colour, scale=1, spacing=1):
        cx = x
        for ch in s.upper():
            rows = GLYPHS.get(ch, GLYPHS["?"]).split()
            for ry, row in enumerate(rows):
                for rx, bit in enumerate(row):
                    if bit == "1":
                        if scale == 1:
                            self.set(cx + rx, y + ry, colour)
                        else:
                            self.rect(
                                cx + rx * scale, y + ry * scale,
                                cx + rx * scale + scale - 1, y + ry * scale + scale - 1,
                                colour,
                            )
            cx += (3 + spacing) * scale

    def text_width(self, s, scale=1, spacing=1):
        return len(s) * (3 + spacing) * scale

    def copy_pixels(self):
        return bytes(self.px)


class View:
    """Maps world sub-units onto canvas pixels."""

    def __init__(self, box, x0, y0, x1, y1):
        self.bx0, self.by0, self.bx1, self.by1 = box
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    def px(self, x):
        return self.x0 + (x - self.bx0) * (self.x1 - self.x0) // (self.bx1 - self.bx0)

    def py(self, y):
        # World y points up; screen y points down.
        return self.y1 - (y - self.by0) * (self.y1 - self.y0) // (self.by1 - self.by0)

    def pr(self, r):
        return max(1, r * (self.x1 - self.x0) // (self.bx1 - self.bx0))
