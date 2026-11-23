#!/usr/bin/env python3
"""Build the 22 November 2026 world-news poster (1024x1024 PNG).

Renders a newspaper front page from the story data embedded below.
Run: python3 build_poster.py  -> writes poster.png next to this file.
Only used at build time; the entry itself (main.py) just ships the PNG.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024
MARGIN = 36

PAPER = (246, 241, 231)
INK = (22, 26, 32)
RED = (179, 39, 30)
GREY = (90, 95, 102)
BAND = (22, 26, 32)
GOLD = (201, 162, 39)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit `width` pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=1.25):
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, label, size=22, color=RED):
    """Small red square + uppercase label; returns y below it."""
    f = font(BOLD, size)
    s = size - 8
    draw.rectangle([x, y + 3, x + s, y + 3 + s], fill=color)
    draw.text((x + s + 10, y), label, font=f, fill=color)
    return y + size + 8


def globe(draw, cx, cy, r, color=INK):
    """Minimal line globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=color, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=2)
    draw.arc([cx - r, cy - int(r * 0.45), cx + r, cy + int(r * 0.45)],
             0, 360, fill=color, width=2)


STORIES = {
    "hero": {
        "kicker": "CLIMATE  ·  ANTALYA, TURKIYE",
        "headline": "COP31 COLLAPSES",
        "deck": "No deal on fossil fuels as the longest climate summit in history ends in failure",
        "body": ("After two weeks and record overtime, the EU and 130+ nations "
                 "refused a pact that never named coal, oil or gas. Guterres: "
                 "\u201cdeeply disappointed.\u201d"),
        "stats": ["LONGEST COP EVER", "190+ NATIONS", "US ABSENT"],
    },
    "gulf": {
        "kicker": "MIDDLE EAST  ·  THE GULF",
        "headline": "GULF ON FIRE",
        "body": ("Iran strikes US bases in Bahrain; a fire hits a Sitra plant, "
                 "two hurt. Two tankers hit mines near Hormuz."),
    },
    "ukraine": {
        "kicker": "EUROPE  ·  UKRAINE",
        "headline": "KYIV PLEADS FOR PATRIOTS",
        "body": ("Zelenskyy urges Washington to release missiles already paid "
                 "for. A Russian strike on a Kyiv flat kills 3."),
    },
    "house": {
        "kicker": "UNITED STATES",
        "headline": "DEMOCRATS TAKE THE HOUSE",
        "body": "Largest House majority since 1992 after a recount.",
    },
    "icj": {
        "kicker": "THE HAGUE",
        "headline": "MYANMAR GUILTY OF GENOCIDE",
        "body": "World court: Myanmar guilty of Rohingya genocide.",
    },
    "sudan": {
        "kicker": "AFRICA  ·  SUDAN",
        "headline": "DRONES KILL 4 NEAR KHARTOUM",
        "body": "RSF-blamed drones kill four; a UN building is hit.",
    },
}

TICKER = ("Russian warship sunk off Libya, Kyiv says  \u2022  Indonesia "
          "factory fire: 3 dead, 34 missing  \u2022  Nigeria boat sinks: "
          "24 dead  \u2022  Europe cost protests, day 3")


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = SIZE - MARGIN
    w = x1 - x0

    # Outer frame.
    d.rectangle([12, 12, SIZE - 13, SIZE - 13], outline=INK, width=3)

    # ---- Masthead ----
    y = 28
    title_f = font(BOLD, 80)
    title = "THE WORLD"
    tw = d.textlength(title, font=title_f)
    d.text(((SIZE - tw) / 2, y), title, font=title_f, fill=INK)
    globe(d, SIZE - 92, 72, 28)
    y += 100
    sub_f = font(BOLD, 24)
    sub = "IN ONE IMAGE  \u2014  SUNDAY, 22 NOVEMBER 2026"
    sw = d.textlength(sub, font=sub_f)
    d.text(((SIZE - sw) / 2, y), sub, font=sub_f, fill=INK)
    y += 40
    rule(d, x0, y, x1, width=4)
    rule(d, x0, y + 7, x1, width=1)
    y += 20

    # ---- Hero story ----
    y = kicker(d, x0, y, STORIES["hero"]["kicker"], size=22)
    hero_f = font(BOLD, 72)
    d.text((x0, y), STORIES["hero"]["headline"], font=hero_f, fill=INK)
    y += int(72 * 1.12)
    rule(d, x0, y + 2, x0 + 120, width=5, fill=RED)
    y += 14
    deck_f = font(BOLD, 28)
    y = draw_wrapped(d, x0, y, STORIES["hero"]["deck"], deck_f, w, INK, 1.22)
    y += 6
    body_f = font(PLAIN, 21)
    y = draw_wrapped(d, x0, y, STORIES["hero"]["body"], body_f, w, INK, 1.3)
    y += 10
    stat_f = font(BOLD, 19)
    stats = "   \u2022   ".join(STORIES["hero"]["stats"])
    sw = d.textlength(stats, font=stat_f)
    d.text(((SIZE - sw) / 2, y), stats, font=stat_f, fill=RED)
    y += 30
    rule(d, x0, y, x1, width=2)
    y += 14

    # ---- Second row: two stories ----
    col_w = (w - 28) // 2
    row2_top = y
    row2_bottom = row2_top
    for i, key in enumerate(("gulf", "ukraine")):
        s = STORIES[key]
        cx = x0 + i * (col_w + 28)
        cy = row2_top
        cy = kicker(d, cx, cy, s["kicker"], size=22)
        hf = font(BOLD, 36)
        cy = draw_wrapped(d, cx, cy, s["headline"], hf, col_w, INK, 1.15)
        cy += 5
        bf = font(PLAIN, 20)
        cy = draw_wrapped(d, cx, cy, s["body"], bf, col_w, INK, 1.32)
        row2_bottom = max(row2_bottom, cy)
    y = row2_bottom + 12
    rule(d, x0, y, x1, width=2)
    y += 14

    # ---- Third row: three stories ----
    col3_w = (w - 48) // 3
    row3_top = y
    row3_bottom = row3_top
    for i, key in enumerate(("house", "icj", "sudan")):
        s = STORIES[key]
        cx = x0 + i * (col3_w + 24)
        cy = row3_top
        cy = kicker(d, cx, cy, s["kicker"], size=20)
        hf = font(BOLD, 27)
        cy = draw_wrapped(d, cx, cy, s["headline"], hf, col3_w, INK, 1.15)
        cy += 4
        bf = font(PLAIN, 18)
        cy = draw_wrapped(d, cx, cy, s["body"], bf, col3_w, INK, 1.3)
        row3_bottom = max(row3_bottom, cy)
    y = row3_bottom + 14

    # ---- Ticker band ----
    band_top = y
    band_h = 64
    d.rectangle([x0, band_top, x1, band_top + band_h], fill=BAND)
    tf = font(BOLD, 19)
    lab = "ALSO TODAY"
    lw = d.textlength(lab, font=tf)
    tick_f = font(PLAIN, 19)
    tx = x0 + 16 + lw + 18
    tw = x1 - 16 - tx
    tlines = wrap(d, TICKER, tick_f, tw)
    lh = int(19 * 1.3)
    total_h = len(tlines) * lh
    ty2 = band_top + (band_h - total_h) // 2
    d.text((x0 + 16, ty2), lab, font=tf, fill=GOLD)
    for line in tlines:
        d.text((tx, ty2), line, font=tick_f, fill=PAPER)
        ty2 += lh
    y = band_top + band_h + 12

    # ---- Footer ----
    foot_f = font(PLAIN, 17)
    foot = "Sources: UN News \u00b7 CNN \u00b7 Reuters \u00b7 AP  \u2014  Sunday 22 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((SIZE - fw) / 2, y), foot, font=foot_f, fill=GREY)
    y += 24
    print(f"layout bottom y={y} (canvas {SIZE})")
    assert y <= SIZE - 8, "layout overflow!"

    out = os.path.join(HERE, "poster.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {size} bytes, {img.size[0]}x{img.size[1]}")
    assert size <= 1024 * 1024, "poster over 1 MiB!"
    assert img.size == (1024, 1024)
    return out


if __name__ == "__main__":
    build()
