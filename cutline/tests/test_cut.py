"""Tests for the cut search, including optimality against exhaustive enumeration."""

from __future__ import annotations

import random
import unittest
from datetime import timedelta

from cutline.cut import brute_force_cut, deferrals, greedy_cut, minimum_cut
from cutline.feasibility import feasible
from tests.support import at, calendar_for, plan_of, random_plan, task


class CutBasicsTest(unittest.TestCase):
    def test_nothing_to_cut_when_the_plan_fits(self):
        plan = plan_of([task("a", 60, at(0, 17))])
        cut = minimum_cut(plan.tasks, calendar_for(plan))
        self.assertEqual(cut.dropped, ())
        self.assertEqual(cut.weight, 0.0)
        self.assertTrue(cut.proven_minimal)
        self.assertTrue(cut.empty)

    def test_cuts_the_cheapest_task(self):
        plan = plan_of(
            [
                task("important", 5 * 60, at(0, 17, 30), weight=5),
                task("optional", 4 * 60, at(0, 17, 30), weight=1),
            ]
        )
        cut = minimum_cut(plan.tasks, calendar_for(plan))
        self.assertEqual(cut.dropped, ("optional",))
        self.assertEqual(cut.weight, 1.0)
        self.assertTrue(cut.proven_minimal)

    def test_prefers_one_expensive_cut_over_two_cheap_ones_when_cheaper(self):
        # Cutting the 6h task alone fixes the plan at weight 2. Cutting both small
        # tasks also fixes it but costs 2.5, so the single cut must win.
        plan = plan_of(
            [
                task("big", 6 * 60, at(0, 17, 30), weight=2),
                task("small one", 2 * 60, at(0, 17, 30), weight=1.25),
                task("small two", 2 * 60, at(0, 17, 30), weight=1.25),
            ]
        )
        calendar = calendar_for(plan)
        cut = minimum_cut(plan.tasks, calendar)
        self.assertEqual(cut.dropped, ("big",))
        self.assertEqual(cut.weight, 2.0)
        self.assertTrue(feasible([t for t in plan.tasks if t.name != "big"], calendar))

    def test_required_tasks_are_never_cut(self):
        plan = plan_of(
            [
                task("must do", 6 * 60, at(0, 17, 30), weight=1, required=True),
                task("could drop", 3 * 60, at(0, 17, 30), weight=9),
            ]
        )
        cut = minimum_cut(plan.tasks, calendar_for(plan))
        self.assertEqual(cut.dropped, ("could drop",))
        self.assertFalse(cut.impossible)

    def test_impossible_when_required_tasks_alone_do_not_fit(self):
        plan = plan_of(
            [
                task("huge", 20 * 60, at(0, 17, 30), required=True),
                task("other", 60, at(0, 17, 30)),
            ]
        )
        cut = minimum_cut(plan.tasks, calendar_for(plan))
        self.assertTrue(cut.impossible)
        self.assertEqual(cut.dropped, ("other",))

    def test_greedy_produces_a_feasible_cut(self):
        plan = plan_of(
            [
                task("a", 4 * 60, at(0, 17, 30)),
                task("b", 4 * 60, at(0, 17, 30)),
                task("c", 4 * 60, at(1, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        dropped = set(greedy_cut(plan.tasks, calendar))
        self.assertTrue(dropped)
        kept = [item for item in plan.tasks if item.name not in dropped]
        self.assertTrue(feasible(kept, calendar))

    def test_budget_exhaustion_is_reported_honestly(self):
        plan = plan_of(
            [task(f"t{index}", 3 * 60, at(0, 17, 30)) for index in range(8)]
        )
        cut = minimum_cut(plan.tasks, calendar_for(plan), node_budget=1)
        self.assertFalse(cut.proven_minimal)
        self.assertTrue(cut.budget_exhausted)
        # The returned cut still works, it just may not be the cheapest.
        kept = [item for item in plan.tasks if item.name not in cut.dropped]
        self.assertTrue(feasible(kept, calendar_for(plan)))

    def test_repeated_runs_are_identical(self):
        plan = plan_of(
            [
                task("a", 4 * 60, at(0, 17, 30), weight=1),
                task("b", 4 * 60, at(0, 17, 30), weight=1),
                task("c", 2 * 60, at(1, 12), weight=1),
            ]
        )
        calendar = calendar_for(plan)
        first = minimum_cut(plan.tasks, calendar)
        second = minimum_cut(plan.tasks, calendar)
        self.assertEqual(first, second)


class CutOptimalityTest(unittest.TestCase):
    """The branch and bound must match exhaustive enumeration, instance by instance."""

    def test_matches_brute_force_on_random_instances(self):
        rng = random.Random(4242)
        compared = 0
        infeasible_seen = 0
        for index in range(150):
            plan = random_plan(rng, rng.randint(2, 7))
            calendar = calendar_for(plan)
            exact = brute_force_cut(plan.tasks, calendar)
            found = minimum_cut(plan.tasks, calendar)
            compared += 1
            if not feasible(plan.tasks, calendar):
                infeasible_seen += 1
            self.assertTrue(found.proven_minimal, f"instance {index} was not proven")
            self.assertAlmostEqual(
                found.weight,
                exact.weight,
                msg=f"instance {index}: search {found.dropped} vs exact {exact.dropped}",
            )
            self.assertEqual(
                found.impossible, exact.impossible, f"instance {index} disagrees"
            )
            if not found.impossible:
                kept = [
                    item for item in plan.tasks if item.name not in found.dropped
                ]
                self.assertTrue(
                    feasible(kept, calendar), f"instance {index} cut is not feasible"
                )
        self.assertGreater(compared, 100)
        self.assertGreater(infeasible_seen, 20, "no infeasible instances were generated")

    def test_matches_brute_force_with_unit_weights(self):
        """With equal weights the answer is the smallest number of tasks to cut."""
        rng = random.Random(11)
        checked = 0
        for _ in range(80):
            plan = random_plan(rng, rng.randint(3, 6))
            tasks = tuple(
                item.__class__(
                    name=item.name,
                    estimate=item.estimate,
                    due=item.due,
                    earliest=item.earliest,
                    weight=1.0,
                    required=False,
                )
                for item in plan.tasks
            )
            plan = plan.with_tasks(tasks)
            calendar = calendar_for(plan)
            if feasible(plan.tasks, calendar):
                continue
            checked += 1
            exact = brute_force_cut(plan.tasks, calendar)
            found = minimum_cut(plan.tasks, calendar)
            self.assertEqual(len(found.dropped), len(exact.dropped))
        self.assertGreater(checked, 10)


class DeferralAdviceTest(unittest.TestCase):
    def test_deferral_makes_the_task_fit_and_one_minute_earlier_does_not(self):
        plan = plan_of(
            [
                task("keep", 6 * 60, at(0, 17, 30)),
                task("cut me", 4 * 60, at(0, 17, 30), weight=0.5),
            ]
        )
        calendar = calendar_for(plan)
        cut = minimum_cut(plan.tasks, calendar)
        self.assertEqual(cut.dropped, ("cut me",))
        limit = calendar.minutes(plan.horizon() + timedelta(days=20))
        advice = deferrals(plan.tasks, calendar, cut, limit)
        moved = advice["cut me"]
        self.assertIsNotNone(moved)
        assert moved is not None

        from dataclasses import replace

        kept = [item for item in plan.tasks if item.name != "cut me"]
        target = plan.task("cut me")
        self.assertTrue(
            feasible(kept + [replace(target, due=calendar.moment(moved))], calendar)
        )
        self.assertFalse(
            feasible(kept + [replace(target, due=calendar.moment(moved - 1))], calendar)
        )

    def test_no_deferral_offered_when_the_plan_is_impossible(self):
        plan = plan_of(
            [
                task("huge", 40 * 60, at(0, 17, 30), required=True),
                task("other", 60, at(0, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        cut = minimum_cut(plan.tasks, calendar)
        self.assertTrue(cut.impossible)
        limit = calendar.minutes(plan.horizon() + timedelta(days=5))
        # Deferral advice is only meaningful for a cut that actually fixes the plan.
        advice = deferrals(plan.tasks, calendar, cut, limit)
        self.assertEqual(set(advice), {"other"})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
