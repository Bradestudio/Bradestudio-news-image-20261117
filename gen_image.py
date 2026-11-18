#!/usr/bin/env python3
"""news-image-20261117 entry: draw the front page of Tuesday 17 Nov 2026.

Build-time generator (run locally with Pillow). It draws a newspaper
front page — masthead, a lead illustration of the Kerch Bridge strike,
and four more stories — and writes entry.png (1024x1024, < 1 MiB).
The shipped main.py only copies that PNG to /output/entry.png, so the
graded program is stdlib-only and byte-deterministic.

Stories (all first reported / happened Tue 17 Nov 2026, any timezone):
  1. LEAD — Ukraine strikes the Kerch Bridge to Crimea; a road span
     collapses, traffic halted (BBC / Al Jazeera).
  2. MIDDLE EAST — Two tankers hit mines and catch fire near the Strait
     of Hormuz; a third US carrier reaches the region (Reuters / Al Jazeera).
  3. ASIA — Trump arrives in Manila for ASEAN; China confirms a
     Xi-Trump-Putin meeting in Shenzhen on Thursday (AP / Outlook India).
  4. EUROPE — Five EU states plan a joint Rwanda return hub for rejected
     asylum seekers (announced Monday, reported 17 Nov).
  5. SPACE — ULA Vulcan fails minutes after liftoff; 40 Amazon Leo
     satellites destroyed (ULA / Spaceflight Now).
Footer also notes: JPMorgan's software-bug banking outage, Russian
strikes on two Kyiv bridges, Nvidia's first post-Huang earnings.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (179, 38, 30)
GREY = (90, 86, 76)
RULE = (60, 56, 48)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------------ scenes

def clip_scene(scene_fn, x0, y0, x1, y1):
    """Draw a scene into a temp image so nothing spills past its panel."""
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(tmp)
    scene_fn(d, 0, 0, w, h)
    return tmp


def draw_lead_scene(draw, x0, y0, x1, y1):
    """Dusk over the strait: a bridge with its middle span broken and
    burning, smoke rising, a tilted section sliding into the water."""
    # Sky: dusk gradient, deep blue-violet to burnt orange at horizon.
    horizon = y0 + int((y1 - y0) * 0.62)
    for y in range(y0, horizon):
        t = (y - y0) / max(1, horizon - y0)
        c = lerp((43, 52, 96), (214, 110, 52), t * t)
        draw.line([(x0, y), (x1, y)], fill=c)
    # Low sun glow.
    sx, sy = x0 + 130, horizon - 26
    for r, a in ((64, 90), (44, 140), (26, 200)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 190, 90))
    # Sea.
    for y in range(horizon, y1):
        t = (y - horizon) / max(1, y1 - horizon)
        c = lerp((38, 58, 88), (18, 28, 50), t)
        draw.line([(x0, y), (x1, y)], fill=c)
    # Sun reflection streaks on the water.
    for i, yy in enumerate(range(horizon + 8, y1 - 8, 14)):
        wdt = 90 - i * 6
        draw.line([(sx - wdt // 2, yy), (sx + wdt // 2, yy)],
                  fill=(255, 170, 80), width=3)
    deck_y = horizon - 58
    # Bridge towers (dark silhouettes).
    for tx in (x0 + 120, x1 - 150):
        draw.rectangle([tx, deck_y - 118, tx + 26, deck_y + 4],
                       fill=(24, 26, 38))
        draw.rectangle([tx - 6, deck_y - 126, tx + 32, deck_y - 118],
                       fill=(24, 26, 38))
    # Cables from towers.
    for tx in (x0 + 133, x1 - 137):
        draw.line([(tx, deck_y - 118), (tx - 150, deck_y)],
                  fill=(24, 26, 38), width=2)
        draw.line([(tx, deck_y - 118), (tx + 150, deck_y)],
                  fill=(24, 26, 38), width=2)
    # Deck: intact left and right spans, gap in the middle.
    gap_l, gap_r = x0 + 400, x0 + 580
    draw.rectangle([x0, deck_y, gap_l, deck_y + 12], fill=(24, 26, 38))
    draw.rectangle([gap_r, deck_y, x1, deck_y + 12], fill=(24, 26, 38))
    # Broken span: tilted down into the water, half-submerged.
    draw.polygon([(gap_l, deck_y), (gap_r - 40, deck_y + 6),
                  (gap_r - 10, deck_y + 78), (gap_l + 18, deck_y + 66)],
                 fill=(30, 32, 46))
    draw.polygon([(gap_l + 18, deck_y + 66), (gap_r - 10, deck_y + 78),
                  (gap_r + 6, deck_y + 96), (gap_l + 34, deck_y + 84)],
                 fill=(16, 18, 30))
    # Splash where the span meets the water.
    for dx, r in ((-14, 12), (0, 17), (16, 11)):
        draw.ellipse([gap_r - 4 + dx - r, deck_y + 82 - r,
                      gap_r - 4 + dx + r, deck_y + 82 + r],
                     outline=(220, 230, 240), width=3)
    # Fire at the break point.
    fx, fy = (gap_l + gap_r) // 2, deck_y - 6
    for r, col in ((36, (255, 120, 20)), (24, (255, 170, 40)),
                   (13, (255, 220, 90))):
        draw.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
    # Smoke column rising from the fire (kept short so it stays inside
    # the panel; the scene is clipped to its rectangle).
    smoke = [(fx - 6, fy - 22, 12), (fx + 10, fy - 40, 15),
             (fx - 2, fy - 56, 18)]
    for (cx, cy, r) in smoke:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(96, 92, 96))
        draw.ellipse([cx - r + 10, cy - r + 8, cx + r - 6, cy + r - 10],
                     fill=(128, 124, 128))
    # Small boats / distant shore at the right edge.
    draw.polygon([(x1 - 90, y1 - 26), (x1 - 30, y1 - 26),
                  (x1 - 44, y1 - 12), (x1 - 76, y1 - 12)], fill=(12, 14, 24))


def draw_tanker(draw, x0, y0, x1, y1):
    """Oil tanker on a dark sea, a mine beside it, flames on deck."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)],
                  fill=lerp((64, 84, 110), (20, 30, 48), t))
    sea_y = y0 + int((y1 - y0) * 0.66)
    draw.rectangle([x0, sea_y, x1, y1], fill=(16, 28, 48))
    # Hull.
    draw.polygon([(x0 + 12, sea_y - 26), (x1 - 12, sea_y - 26),
                  (x1 - 30, sea_y + 6), (x0 + 30, sea_y + 6)],
                 fill=(120, 30, 26))
    draw.rectangle([x0 + 18, sea_y - 52, x0 + 66, sea_y - 26],
                   fill=(200, 200, 200))
    draw.rectangle([x0 + 76, sea_y - 44, x0 + 92, sea_y - 26],
                   fill=(200, 200, 200))
    # Flames on deck.
    for (fx, r, col) in ((x0 + 118, 16, (255, 140, 30)),
                         (x0 + 136, 11, (255, 200, 60))):
        draw.ellipse([fx - r, sea_y - 52 - r, fx + r, sea_y - 52 + r],
                     fill=col)
    # Naval mine: spiked ball floating nearby.
    mx, my = x1 - 42, sea_y - 6
    draw.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(30, 30, 34))
    for ang in range(0, 360, 45):
        import math
        dx = int(17 * math.cos(math.radians(ang)))
        dy = int(17 * math.sin(math.radians(ang)))
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(30, 30, 34),
                  width=3)


def draw_summit(draw, x0, y0, x1, y1):
    """Three flags on poles above a podium: US, China, Russia (abstract
    stripes in each flag's colours)."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)],
                  fill=lerp((240, 236, 222), (214, 206, 188), t))
    poles = [x0 + 18, (x0 + x1) // 2 - 15, x1 - 48]
    flags = [((178, 34, 52), (255, 255, 255), (60, 60, 120)),   # US
             ((222, 41, 16), (255, 222, 0), None),               # China
             ((255, 255, 255), (0, 57, 166), (213, 0, 50))]     # Russia
    for px, (c1, c2, c3) in zip(poles, flags):
        draw.rectangle([px - 2, y0 + 18, px + 2, y1 - 34], fill=(60, 52, 40))
        fy = y0 + 18
        if c3 is None:  # China: red field, yellow stars (dots).
            draw.rectangle([px + 2, fy, px + 32, fy + 30], fill=c1)
            for (sx, sy) in ((px + 10, fy + 9), (px + 18, fy + 7),
                             (px + 23, fy + 14), (px + 18, fy + 20)):
                draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=c2)
        else:  # horizontal tricolour.
            draw.rectangle([px + 2, fy, px + 32, fy + 10], fill=c1)
            draw.rectangle([px + 2, fy + 10, px + 32, fy + 20], fill=c2)
            draw.rectangle([px + 2, fy + 20, px + 32, fy + 30], fill=c3)
    # Podium.
    draw.polygon([(x0 + 26, y1 - 34), (x1 - 26, y1 - 34),
                  (x1 - 44, y1 - 6), (x0 + 44, y1 - 6)], fill=(70, 60, 48))
    draw.rectangle([x0 + 26, y1 - 40, x1 - 26, y1 - 34], fill=(90, 78, 62))


def draw_hub(draw, x0, y0, x1, y1):
    """A plane flying over a simplified map: Europe top-left, a dashed
    route arrow down to a marked Rwanda in east Africa."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)],
                  fill=lerp((222, 232, 226), (196, 212, 200), t))
    # Stylised Africa silhouette (abstract polygon).
    draw.polygon([(x0 + 62, y0 + 18), (x1 - 30, y0 + 14),
                  (x1 - 18, y0 + 52), (x1 - 52, y0 + 108),
                  (x0 + 96, y0 + 118), (x0 + 58, y0 + 66)],
                 fill=(168, 152, 104))
    # Europe blob.
    draw.ellipse([x0 + 48, y0 + 6, x0 + 96, y0 + 34], fill=(120, 132, 110))
    # Dashed route arrow Europe -> Rwanda.
    import math
    ax, ay = x0 + 74, y0 + 30
    bx, by = x1 - 46, y0 + 92
    steps = 14
    for i in range(steps):
        if i % 2:
            continue
        t0 = i / steps
        t1 = (i + 1) / steps
        draw.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0),
                   (ax + (bx - ax) * t1, ay + (by - ay) * t1)],
                  fill=RED, width=4)
    # Destination marker.
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], outline=RED, width=4)
    draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)
    # Small plane at the route's start.
    px, py = x0 + 58, y0 + 22
    draw.polygon([(px, py - 8), (px + 26, py), (px, py + 8),
                  (px + 6, py)], fill=(40, 44, 56))
    draw.polygon([(px + 4, py - 3), (px + 16, py - 14), (px + 20, py - 3)],
                 fill=(40, 44, 56))


def draw_rocket(draw, x0, y0, x1, y1):
    """A rocket breaking apart against a starry sky, debris and a
    small satellite tumbling below."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)],
                  fill=lerp((12, 16, 38), (52, 40, 78), t))
    import math
    state = 4242
    for _ in range(40):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        sx = x0 + state % (x1 - x0)
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        sy = y0 + state % (y1 - y0)
        draw.point((sx, sy), fill=(220, 220, 240))
    cx = (x0 + x1) // 2
    # Rocket body, tilted, breaking: nose cone up-left, body down-right.
    draw.polygon([(cx - 6, y0 + 16), (cx + 10, y0 + 30),
                  (cx - 2, y0 + 52), (cx - 16, y0 + 38)], fill=(220, 224, 230))
    draw.polygon([(cx - 14, y0 + 46), (cx + 2, y0 + 60),
                  (cx - 10, y0 + 96), (cx - 26, y0 + 82)], fill=(200, 60, 40))
    # Explosion flash at the break.
    ex, ey = cx - 4, y0 + 54
    for r, col in ((30, (255, 140, 30)), (18, (255, 200, 80)),
                   (9, (255, 240, 160))):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    # Debris pieces.
    for (dx, dy, s) in ((-38, 26, 7), (30, 34, 6), (-22, 58, 5),
                        (36, 62, 8), (6, 78, 5)):
        draw.rectangle([cx + dx - s, ey + dy - s, cx + dx + s,
                        ey + dy + s], fill=(180, 180, 190))
    # Tumbling satellite (small box + panels) below.
    sx, sy = x1 - 34, y1 - 30
    draw.rectangle([sx - 8, sy - 6, sx + 8, sy + 6], fill=(150, 160, 180))
    draw.rectangle([sx - 26, sy - 3, sx - 8, sy + 3], fill=(40, 90, 180))
    draw.rectangle([sx + 8, sy - 3, sx + 26, sy + 3], fill=(40, 90, 180))


# ------------------------------------------------------------------ page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Double border frame.
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    draw.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # ---- Masthead ----
    draw_center(draw, 34, "THE WORLD TODAY",
                font(SERIF_B, 66))
    draw.rectangle([150, 118, W - 150, 120], fill=RULE)
    draw_center(draw, 128, "TUESDAY, 17 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
                font(SANS_B, 19))
    draw.rectangle([150, 156, W - 150, 158], fill=RULE)

    # ---- Lead story ----
    draw_center(draw, 168, "UKRAINE  ·  LEAD STORY", font(SANS_B, 18),
                fill=RED)
    img.paste(clip_scene(draw_lead_scene, 30, 196, W - 30, 428), (30, 196))
    draw.rectangle([30, 196, W - 30, 428], outline=INK, width=2)
    draw_center(draw, 440, "KERCH BRIDGE HIT —", font(SERIF_B, 52))
    draw_center(draw, 496, "SPAN COLLAPSES", font(SERIF_B, 52))
    deck = ("Ukraine strikes the Crimea link for the second day running — "
            "a road span falls into the strait and traffic is halted. "
            "Moscow vows to rebuild.")
    for i, line in enumerate(wrap(draw, deck, font(SERIF, 21), 900)):
        draw_center(draw, 556 + i * 26, line, font(SERIF, 21))
    draw.rectangle([150, 612, W - 150, 614], fill=RULE)

    # ---- Four stories, 2x2 grid ----
    stories = [
        ("MIDDLE EAST", "TANKERS HIT BY MINES NEAR HORMUZ",
         "Two tankers catch fire after striking mines near the strait. "
         "A third US carrier, USS Theodore Roosevelt, reaches the region.",
         draw_tanker),
        ("ASIA", "TRUMP IN MANILA; XI, TRUMP, PUTIN TO MEET",
         "Trump lands in Manila for ASEAN, then heads to Shenzhen for "
         "three-way talks with Xi and Putin on Thursday.", draw_summit),
        ("EUROPE", "FIVE EU STATES PLAN RWANDA RETURN HUB",
         "Germany, Denmark, Austria, Greece and the Netherlands will send "
         "rejected asylum seekers to a joint facility from next year.",
         draw_hub),
        ("SPACE", "VULCAN ROCKET FAILS — 40 SATELLITES LOST",
         "A ULA Vulcan rocket breaks up ten minutes after liftoff from "
         "Cape Canaveral, destroying 40 Amazon Leo satellites.",
         draw_rocket),
    ]
    gx, gy = 30, 628
    cw, ch, gap = 472, 152, 16
    f_kick = font(SANS_B, 15)
    f_head = font(SANS_B, 23)
    f_body = font(SANS, 16)
    for idx, (kick, head, body, scene) in enumerate(stories):
        cx = gx + (idx % 2) * (cw + gap)
        cy = gy + (idx // 2) * (ch + gap)
        # Icon panel (clipped so the drawing never spills into the text).
        img.paste(clip_scene(scene, cx, cy, cx + 150, cy + 150), (cx, cy))
        draw.rectangle([cx, cy, cx + 150, cy + 150], outline=INK, width=2)
        tx = cx + 164
        tw = cw - 164
        draw.text((tx, cy + 2), kick, font=f_kick, fill=RED)
        y = cy + 24
        for line in wrap(draw, head, f_head, tw):
            draw.text((tx, y), line, font=f_head, fill=INK)
            y += 27
        y += 2
        for line in wrap(draw, body, f_body, tw):
            draw.text((tx, y), line, font=f_body, fill=(40, 38, 32))
            y += 20

    # ---- Footer ----
    draw.rectangle([150, 956, W - 150, 958], fill=RULE)
    draw_center(draw, 964,
                "ALSO: JPMorgan blames a software bug for Monday's banking "
                "outage · Russian missiles hit two bridges in Kyiv",
                font(SANS, 14), fill=GREY)
    draw_center(draw, 982,
                "Nvidia reports its first earnings since Jensen Huang's exit",
                font(SANS, 14), fill=GREY)
    return img


def main():
    out = os.environ.get("ENTRY_OUT", "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size,
          os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
