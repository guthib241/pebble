"""Build the demo animations.

Run from the project root:

    python3 demo/make_demo.py

Writes demo/rewind.gif and demo/billiards.gif, and prints what it measured while
doing so. Nothing here invents a figure. The round-trip line is a comparison of the
actual integer state before and after, and the script refuses to write a GIF if the
reverse run does not land exactly on the start state.

Note on the trail: the comet tail behind each ball is drawn for the viewer, from
positions this script sampled for that purpose. The simulation itself stores no
frames -- the only thing it keeps in order to go backwards is the residue tape,
whose measured size is printed below.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ebb.gif import write_gif
from ebb.render import Canvas, View
from ebb import scenes

W, H = 340, 220
PALETTE = [
    (16, 18, 24),      # 0 background
    (48, 55, 71),      # 1 box and ghosts
    (38, 74, 88),      # 2 trail, far
    (96, 186, 204),    # 3 trail, near
    (150, 162, 184),   # 4 label
    (236, 180, 84),    # 5 accent, forward
    (122, 198, 146),   # 6 accent, reverse
    (226, 108, 92), (236, 168, 88), (238, 214, 110), (150, 206, 132),
    (112, 196, 198), (124, 166, 232), (176, 146, 230), (230, 140, 186),
    (240, 240, 245),   # 15 white
]
BODY_COLOURS = list(range(7, 15))
WINDOW = 26  # trail samples shown behind (forward) or ahead (reverse) of each ball


def draw(world, view, trail, idx, phase, step_no, total_steps, note, ghosts):
    c = Canvas(W, H, 0)
    c.frame(view.x0 - 1, view.y0 - 1, view.x1 + 1, view.y1 + 1, 1)

    for gx, gy, gr in ghosts:
        c.ring(gx, gy, gr, 1)

    lo = max(1, idx - WINDOW)
    for pts in trail:
        upper = min(idx, len(pts) - 1)
        for k in range(lo, upper + 1):
            x0, y0 = pts[k - 1]
            x1, y1 = pts[k]
            if abs(x1 - x0) + abs(y1 - y0) > 60:
                continue  # a bounce happened between samples; no false chord
            near = k > upper - WINDOW // 2
            c.line(x0, y0, x1, y1, 3 if near else 2)

    for i in range(len(world)):
        px, py = view.px(world.x[i]), view.py(world.y[i])
        c.disc(px, py, view.pr(world.r[i]), BODY_COLOURS[i % len(BODY_COLOURS)])
        c.set(px, py, 15)

    accent = 5 if phase == "FORWARD" else 6
    c.text(6, 6, "EBB", 15, scale=2)
    c.text(44, 8, phase, accent, scale=2)
    c.text(W - 116, 8, "STEP %5d" % step_no, 4, scale=1)
    c.text(W - 116, 16, note, 4, scale=1)

    bar_y = H - 10
    c.hspan(6, W - 7, bar_y, 1)
    filled = 6 + (W - 13) * step_no // max(1, total_steps)
    c.hspan(6, filled, bar_y, accent)
    c.hspan(6, filled, bar_y - 1, accent)
    return c.copy_pixels()


def rewind_gif(path, scene_fn, steps, sample, hold=10):
    world = scene_fn()
    view = View(world.box, 8, 26, W - 9, H - 24)
    start = world.state()
    n = len(world)
    ghosts = [(view.px(world.x[i]), view.py(world.y[i]), view.pr(world.r[i]))
              for i in range(n)]
    trail = [[] for _ in range(n)]

    def record():
        for i in range(n):
            trail[i].append((view.px(world.x[i]), view.py(world.y[i])))

    record()
    frames = [draw(world, view, trail, 0, "FORWARD", 0, steps, "NO FRAMES STORED", ghosts)]
    delays = [70]
    for s in range(1, steps + 1):
        world.step()
        if s % sample == 0:
            record()
            frames.append(draw(world, view, trail, len(trail[0]) - 1, "FORWARD", s,
                               steps, "NO FRAMES STORED", ghosts))
            delays.append(6)

    forward_count = len(frames)
    end_state = world.state()
    contacts = world.contacts_resolved
    tape_bytes = world.tape.bytes_serialised()
    tape_entries = len(world.tape)

    idx = len(trail[0]) - 1
    frames.append(draw(world, view, trail, idx, "REVERSE", steps, steps,
                       "RUNNING BACKWARDS", ghosts))
    delays.append(70)
    for s in range(steps - 1, -1, -1):
        world.unstep()
        if s % sample == 0:
            idx -= 1
            frames.append(draw(world, view, trail, idx, "REVERSE", s, steps,
                               "RUNNING BACKWARDS", ghosts))
            delays.append(6)

    recovered = world.state() == start
    if not recovered:
        raise SystemExit("round trip was not exact: refusing to write a demo that lies")

    final = draw(world, view, trail, 0, "REVERSE", 0, steps, "EXACT START STATE", ghosts)
    frames += [final] * hold
    delays += [12] * hold

    size = write_gif(path, frames, PALETTE, W, H, delays)
    return {
        "path": path, "bodies": n, "steps": steps, "frames": len(frames),
        "forward_frames": forward_count, "gif_bytes": size, "contacts": contacts,
        "tape_entries": tape_entries, "tape_bytes": tape_bytes,
        "tape_bits_per_contact": round(8 * tape_bytes / contacts, 2) if contacts else 0,
        "snapshot_bytes_per_frame": world.snapshot_bytes_per_frame(),
        "snapshot_bytes_for_full_rewind": world.snapshot_bytes_per_frame() * steps,
        "round_trip_exact": recovered,
        "tape_empty_after_reverse": len(world.tape) == 0,
        "moved_during_run": end_state != start,
    }


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    results = [
        rewind_gif(os.path.join(here, "rewind.gif"),
                   lambda: scenes.drop(seed=7, n=8), steps=2400, sample=24),
        rewind_gif(os.path.join(here, "billiards.gif"),
                   lambda: scenes.billiards(seed=3, n=6), steps=2400, sample=24),
    ]
    for r in results:
        print(os.path.basename(r["path"]) + ":")
        for k, v in r.items():
            if k != "path":
                print("  %-32s %s" % (k, v))
    return results


if __name__ == "__main__":
    main()
