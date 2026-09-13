"""Tests for the rasteriser and the world-to-pixel mapping."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ebb.fixed import fx, varint_len, zigzag
from ebb.render import GLYPHS, Canvas, View


class TestCanvas(unittest.TestCase):
    def test_blank_canvas(self):
        c = Canvas(5, 3, 2)
        self.assertEqual(len(c.px), 15)
        self.assertEqual(set(c.px), {2})

    def test_set_and_clip(self):
        c = Canvas(4, 4, 0)
        c.set(1, 2, 7)
        self.assertEqual(c.px[2 * 4 + 1], 7)
        c.set(-1, 0, 9)
        c.set(0, 99, 9)
        c.set(4, 0, 9)
        self.assertNotIn(9, c.px)

    def test_hspan_clips_to_the_canvas(self):
        c = Canvas(6, 2, 0)
        c.hspan(-5, 99, 0, 3)
        self.assertEqual(list(c.px[:6]), [3] * 6)
        self.assertEqual(list(c.px[6:]), [0] * 6)
        c.hspan(0, 5, 7, 4)  # off-canvas row, must be ignored
        self.assertNotIn(4, c.px)

    def test_disc_is_round_and_centred(self):
        c = Canvas(21, 21, 0)
        c.disc(10, 10, 5, 1)
        self.assertEqual(c.px[10 * 21 + 10], 1)
        self.assertEqual(c.px[10 * 21 + 15], 1)   # on the rim
        self.assertEqual(c.px[10 * 21 + 16], 0)   # outside
        self.assertEqual(c.px[(10 - 4) * 21 + 10 - 3], 1)
        painted = sum(1 for p in c.px if p == 1)
        self.assertGreater(painted, 60)   # a disc of r=5 covers ~81 px
        self.assertLess(painted, 100)

    def test_line_endpoints_and_continuity(self):
        c = Canvas(30, 20, 0)
        c.line(2, 3, 27, 17, 5)
        self.assertEqual(c.px[3 * 30 + 2], 5)
        self.assertEqual(c.px[17 * 30 + 27], 5)
        painted = [(i % 30, i // 30) for i, p in enumerate(c.px) if p == 5]
        painted.sort()
        for (x0, y0), (x1, y1) in zip(painted, painted[1:]):
            self.assertLessEqual(max(abs(x1 - x0), abs(y1 - y0)), 1)

    def test_text_draws_and_stays_inside(self):
        c = Canvas(40, 10, 0)
        c.text(1, 1, "AB 9", 6)
        self.assertIn(6, c.px)
        c2 = Canvas(40, 10, 0)
        c2.text(38, 8, "WWWW", 6)  # runs off the edge, must not raise

    def test_every_glyph_is_three_by_five(self):
        for ch, spec in GLYPHS.items():
            rows = spec.split()
            self.assertEqual(len(rows), 5, ch)
            for row in rows:
                self.assertEqual(len(row), 3, ch)
                self.assertTrue(set(row) <= {"0", "1"}, ch)

    def test_unknown_character_does_not_raise(self):
        Canvas(20, 10, 0).text(0, 0, "é~", 1)


class TestView(unittest.TestCase):
    def test_corners_map_to_corners(self):
        box = (0, 0, fx(10), fx(8))
        v = View(box, 10, 20, 110, 100)
        self.assertEqual(v.px(0), 10)
        self.assertEqual(v.px(fx(10)), 110)
        self.assertEqual(v.py(0), 100)       # world y up, screen y down
        self.assertEqual(v.py(fx(8)), 20)

    def test_radius_never_vanishes(self):
        v = View((0, 0, fx(10), fx(8)), 0, 0, 100, 80)
        self.assertGreaterEqual(v.pr(1), 1)
        self.assertEqual(v.pr(fx(1)), 10)


class TestFixedHelpers(unittest.TestCase):
    def test_zigzag_keeps_small_values_small(self):
        self.assertEqual(zigzag(0), 0)
        self.assertEqual(zigzag(-1), 1)
        self.assertEqual(zigzag(1), 2)

    def test_varint_len_matches_the_encoding_boundaries(self):
        self.assertEqual(varint_len(0), 1)
        self.assertEqual(varint_len(63), 1)      # zigzag 126, fits in 7 bits
        self.assertEqual(varint_len(64), 2)      # zigzag 128, needs 8
        self.assertEqual(varint_len(-64), 1)     # zigzag 127, still fits
        self.assertEqual(varint_len(-65), 2)     # zigzag 129, does not
        self.assertEqual(varint_len(1 << 20), 4)


if __name__ == "__main__":
    unittest.main()
