"""Tests for the hand-written GIF writer.

The encoder is checked against a decoder written from the GIF specification rather
than against itself: the decoder maintains its own LZW table and does not share code
with the encoder, so a wrong code-size bump shows up as a mismatch.

An optional check against Pillow runs when Pillow happens to be installed; it is
skipped otherwise, and the project does not depend on it.
"""

import os
import random
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ebb.gif import lzw_decode, lzw_encode, read_sub_blocks, write_gif
from ebb.render import Canvas


def decode_gif(path):
    """Decode a GIF written by :func:`write_gif`. Returns (w, h, palette, frames)."""
    with open(path, "rb") as fh:
        data = fh.read()
    assert data[:6] == b"GIF89a"
    width, height = struct.unpack("<HH", data[6:10])
    packed = data[10]
    assert packed & 0x80, "expected a global colour table"
    table_size = 1 << ((packed & 0x07) + 1)
    pos = 13
    palette = [tuple(data[pos + 3 * i : pos + 3 * i + 3]) for i in range(table_size)]
    pos += 3 * table_size
    frames, delays = [], []
    while pos < len(data):
        marker = data[pos]
        if marker == 0x3B:
            break
        if marker == 0x21:  # extension
            label = data[pos + 1]
            pos += 2
            if label == 0xF9:
                size = data[pos]
                delays.append(struct.unpack("<H", data[pos + 2 : pos + 4])[0])
                pos += size + 1
                assert data[pos] == 0
                pos += 1
            else:
                _, pos = read_sub_blocks(data, pos + data[pos] + 1)
        elif marker == 0x2C:  # image descriptor
            fx, fy, fw, fh = struct.unpack("<HHHH", data[pos + 1 : pos + 9])
            local = data[pos + 9]
            assert local & 0x80 == 0, "expected no local colour table"
            pos += 10
            min_code_size = data[pos]
            pos += 1
            payload, pos = read_sub_blocks(data, pos)
            pixels = lzw_decode(payload, min_code_size)
            assert (fx, fy, fw, fh) == (0, 0, width, height)
            frames.append(pixels)
        else:
            raise AssertionError("unexpected block 0x%02x at %d" % (marker, pos))
    return width, height, palette, frames, delays


class TestLZW(unittest.TestCase):
    def test_round_trip_on_random_data(self):
        rnd = random.Random(1)
        for trial in range(6):
            n_colours = rnd.choice([4, 16, 64, 256])
            min_code_size = max(2, (n_colours - 1).bit_length())
            data = bytes(rnd.randrange(n_colours) for _ in range(rnd.randint(1, 5000)))
            with self.subTest(trial=trial, colours=n_colours):
                self.assertEqual(lzw_decode(lzw_encode(data, min_code_size), min_code_size), data)

    def test_round_trip_on_flat_data(self):
        data = bytes([5]) * 9000
        self.assertEqual(lzw_decode(lzw_encode(data, 4), 4), data)

    def test_round_trip_past_the_dictionary_limit(self):
        """Long, high-entropy data forces a table reset at 4096 codes."""
        rnd = random.Random(7)
        data = bytes(rnd.randrange(256) for _ in range(80_000))
        self.assertEqual(lzw_decode(lzw_encode(data, 8), 8), data)

    def test_single_pixel(self):
        self.assertEqual(lzw_decode(lzw_encode(b"\x03", 4), 4), b"\x03")


class TestWriteGif(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_tmp_test.gif"
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_frames_decode_to_exactly_what_was_encoded(self):
        rnd = random.Random(4)
        w, h = 41, 27
        palette = [(i * 7 % 256, i * 31 % 256, i * 53 % 256) for i in range(16)]
        frames = [bytes(rnd.randrange(16) for _ in range(w * h)) for _ in range(4)]
        write_gif(self.path, frames, palette, w, h, 5)
        dw, dh, dpal, dframes, delays = decode_gif(self.path)
        self.assertEqual((dw, dh), (w, h))
        self.assertEqual(dpal[:16], palette)
        self.assertEqual(dframes, frames)
        self.assertEqual(delays, [5] * 4)

    def test_per_frame_delays(self):
        w = h = 8
        frames = [bytes([0]) * (w * h), bytes([1]) * (w * h)]
        write_gif(self.path, frames, [(0, 0, 0), (255, 255, 255)], w, h, [30, 7])
        _, _, _, _, delays = decode_gif(self.path)
        self.assertEqual(delays, [30, 7])

    def test_drawn_canvas_survives_the_round_trip(self):
        c = Canvas(60, 40, 0)
        c.frame(0, 0, 59, 39, 1)
        c.disc(30, 20, 9, 2)
        c.line(2, 2, 57, 37, 3)
        c.text(4, 30, "EBB 01", 3)
        frame = c.copy_pixels()
        write_gif(self.path, [frame], [(0, 0, 0), (9, 9, 9), (7, 7, 7), (5, 5, 5)], 60, 40, 4)
        _, _, _, frames, _ = decode_gif(self.path)
        self.assertEqual(frames[0], frame)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            write_gif(self.path, [], [(0, 0, 0)], 4, 4, 5)
        with self.assertRaises(ValueError):
            write_gif(self.path, [bytes(3)], [(0, 0, 0)], 4, 4, 5)
        with self.assertRaises(ValueError):
            write_gif(self.path, [bytes(16)], [(0, 0, 0)] * 300, 4, 4, 5)
        with self.assertRaises(ValueError):
            write_gif(self.path, [bytes(16), bytes(16)], [(0, 0, 0)], 4, 4, [5])

    def test_optional_check_against_an_external_decoder(self):
        try:
            from PIL import Image, ImageSequence
        except ImportError:
            self.skipTest("Pillow not installed; the specification decoder above covers this")
        rnd = random.Random(12)
        w, h = 33, 21
        palette = [(i * 11 % 256, i * 29 % 256, i * 67 % 256) for i in range(16)]
        frames = [bytes(rnd.randrange(16) for _ in range(w * h)) for _ in range(3)]
        write_gif(self.path, frames, palette, w, h, 6)
        im = Image.open(self.path)
        for k, got in enumerate(ImageSequence.Iterator(im)):
            want = b"".join(bytes(palette[i]) for i in frames[k])
            self.assertEqual(got.convert("RGB").tobytes(), want)


if __name__ == "__main__":
    unittest.main()
