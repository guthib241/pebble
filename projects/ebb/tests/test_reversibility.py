"""The claims this project makes are exactness claims, so these tests are exact.

Nothing here compares floats with a tolerance: every assertion is integer equality
of the whole state, or an exhaustive enumeration.
"""

import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ebb import scenes
from ebb.fixed import SCALE, fx
from ebb.world import TapeError, TooFast, World, drift_axis, undrift_axis


class TestWallRule(unittest.TestCase):
    """The wall rule is the smallest place the design can go wrong, so it is
    checked by enumeration rather than by example."""

    def test_exhaustively_injective_and_invertible(self):
        lo, hi = 0, 40
        span = hi - lo
        seen = {}
        for x in range(lo, hi + 1):
            for v in range(-span, span + 1):
                out = drift_axis(x, v, lo, hi)
                self.assertNotIn(out, seen,
                                 "two states collide: %s and %s both -> %s"
                                 % ((x, v), seen.get(out), out))
                seen[out] = (x, v)
                self.assertEqual(undrift_axis(out[0], out[1], lo, hi), (x, v))

    def test_offset_lattice_is_what_makes_it_injective(self):
        """The naive mirror (reflect about the wall itself) is not injective.

        This test pins the reason the rule is written the way it is: if someone
        'simplifies' the +1 away, this fails.
        """
        lo, hi = 0, 40

        def naive(x, v):
            t = x + v
            if t > hi:
                return 2 * hi - t, -v
            if t < lo:
                return 2 * lo - t, -v
            return t, v

        seen = {}
        collisions = 0
        reach = 8
        for x in range(lo, hi + 1):
            for v in range(-reach, reach + 1):
                out = naive(x, v)
                if out in seen and seen[out] != (x, v):
                    collisions += 1
                seen[out] = (x, v)
        self.assertGreater(collisions, 0)

    def test_stays_inside_the_box(self):
        lo, hi = 5, 25
        for x in range(lo, hi + 1):
            for v in range(-(hi - lo), hi - lo + 1):
                nx, _ = drift_axis(x, v, lo, hi)
                self.assertTrue(lo <= nx <= hi)

    def test_too_fast_raises(self):
        with self.assertRaises(TooFast):
            drift_axis(10, 10_000, 0, 20)


class TestRoundTrip(unittest.TestCase):
    def assert_round_trip(self, world, steps):
        start = world.state()
        world.run(steps)
        moved = world.state() != start
        world.unrun(steps)
        self.assertEqual(world.state(), start, "reverse run did not land on the start state")
        self.assertEqual(len(world.tape), 0, "residue tape was not emptied")
        return moved

    def test_drop_scene_10000_steps(self):
        w = scenes.drop()
        self.assertTrue(self.assert_round_trip(w, 10_000))
        self.assertGreater(w.contacts_resolved, 0)

    def test_billiards_scene_10000_steps(self):
        w = scenes.billiards()
        self.assertTrue(self.assert_round_trip(w, 10_000))

    def test_drop_scene_100000_steps(self):
        """A long run, because a bijection that only holds for a while is not one."""
        w = scenes.drop()
        self.assertTrue(self.assert_round_trip(w, 100_000))

    def test_scatter_scene(self):
        self.assertTrue(self.assert_round_trip(scenes.scatter(), 3_000))

    def test_single_body_scene_keeps_the_tape_empty(self):
        """A scene with no pair contact should store literally nothing."""
        w = scenes.single()
        start = w.state()
        w.run(5_000)
        self.assertEqual(len(w.tape), 0)
        self.assertEqual(w.tape.bytes_serialised(), 0)
        self.assertEqual(w.contacts_resolved, 0)
        w.unrun(5_000)
        self.assertEqual(w.state(), start)

    def test_random_scenes(self):
        for seed in range(12):
            rnd = random.Random(seed)
            w = World.from_units((0, 0, 10, 7), gravity=(0.0, -rnd.choice([0.0, 0.002, 0.006])))
            for _ in range(rnd.randint(2, 9)):
                w.add_disc_units(rnd.uniform(1, 9), rnd.uniform(1, 6),
                                 rnd.uniform(-0.09, 0.09), rnd.uniform(-0.09, 0.09),
                                 rnd.choice([0.3, 0.45, 0.6]))
            with self.subTest(seed=seed):
                self.assert_round_trip(w, 900)

    def test_partial_rewind_lands_on_the_right_intermediate_state(self):
        """Rewinding part of the way must land on that frame, not just the start."""
        w = scenes.drop(seed=3)
        w.run(400)
        marked = w.state()
        w.run(600)
        w.unrun(600)
        self.assertEqual(w.state(), marked)
        w.run(600)
        w.unrun(1000)

    def test_step_unstep_step_is_stable(self):
        w = scenes.billiards(seed=9)
        w.run(250)
        a = w.state()
        w.step()
        w.unstep()
        self.assertEqual(w.state(), a)
        w.unstep()
        w.step()
        self.assertEqual(w.state(), a)

    def test_coincident_centres_are_skipped_symmetrically(self):
        w = World.from_units((0, 0, 10, 10))
        w.add_disc_units(5, 5, 0.01, 0.0, 0.5)
        w.add_disc_units(5, 5, -0.01, 0.0, 0.5)
        start = w.state()
        w.run(60)
        w.unrun(60)
        self.assertEqual(w.state(), start)


class TestDeterminism(unittest.TestCase):
    def test_two_runs_of_the_same_scene_agree_exactly(self):
        a, b = scenes.drop(), scenes.drop()
        a.run(2_000)
        b.run(2_000)
        self.assertEqual(a.state(), b.state())
        self.assertEqual(a.tape.items, b.tape.items)

    def test_state_is_integers_only(self):
        w = scenes.drop()
        w.run(500)
        for seq in (w.x, w.y, w.vx, w.vy):
            for value in seq:
                self.assertIsInstance(value, int)
        for value in w.tape.items:
            self.assertIsInstance(value, int)


class TestPhysics(unittest.TestCase):
    def test_contact_conserves_momentum_exactly(self):
        """The impulse is applied equal and opposite as integers, so momentum is
        conserved to the last bit -- not approximately."""
        w = World.from_units((0, 0, 12, 8))
        w.add_disc_units(5.0, 4.0, 0.05, 0.01, 0.5)
        w.add_disc_units(5.7, 4.0, -0.04, 0.0, 0.5)
        before = w.momentum()
        w._contacts(1)
        self.assertEqual(w.momentum(), before)
        self.assertEqual(w.contacts_resolved, 1)

    def test_head_on_equal_masses_exchange_velocity(self):
        w = World.from_units((0, 0, 12, 8))
        w.add_disc_units(5.0, 4.0, 0.05, 0.0, 0.5)
        w.add_disc_units(5.9, 4.0, -0.05, 0.0, 0.5)
        w._contacts(1)
        self.assertLess(w.vx[0], 0)
        self.assertGreater(w.vx[1], 0)
        self.assertEqual(abs(w.vx[0]), abs(w.vx[1]))

    def test_elastic_scene_does_not_gain_or_lose_energy_materially(self):
        """Control: with no gravity, kinetic energy is the whole energy budget.

        Integer rounding in contact perturbs it slightly; this pins how slightly,
        so a future change that starts pumping energy is caught.
        """
        w = scenes.billiards(seed=3)
        e0 = w.kinetic_energy()
        w.run(4_000)
        drift = abs(w.kinetic_energy() - e0) / e0
        self.assertLess(drift, 0.01, "elastic scene drifted by %.4f%%" % (100 * drift))

    def test_bodies_stay_inside_the_box(self):
        w = scenes.scatter()
        for _ in range(1_500):
            w.step()
            self.assertTrue(w.inside())

    def test_a_body_faster_than_the_box_raises(self):
        w = World.from_units((0, 0, 4, 4))
        w.add_disc_units(2, 2, 50.0, 0.0, 0.25)
        with self.assertRaises(TooFast):
            w.step()


class TestTape(unittest.TestCase):
    def test_unstep_without_the_tape_is_refused(self):
        w = scenes.drop()
        w.run(300)
        self.assertGreater(len(w.tape), 0)
        w.tape.items = []
        with self.assertRaises(TapeError):
            w.unrun(300)

    def test_tape_grows_only_with_contacts(self):
        w = scenes.drop()
        w.run(1_000)
        self.assertEqual(len(w.tape), w.contacts_resolved)

    def test_tape_is_far_smaller_than_snapshotting_the_same_run(self):
        """A measured comparison, using the same encoding for both sides."""
        w = scenes.drop()
        steps = 2_000
        w.run(steps)
        tape = w.tape.bytes_serialised()
        snapshots = w.snapshot_bytes_per_frame() * steps
        self.assertGreater(snapshots, tape)
        self.assertGreater(snapshots / max(1, tape), 10)


class TestFixed(unittest.TestCase):
    def test_scale_round_trip(self):
        self.assertEqual(fx(1.0), SCALE)
        self.assertEqual(fx(-2.5), -2 * SCALE - SCALE // 2)


if __name__ == "__main__":
    unittest.main()
