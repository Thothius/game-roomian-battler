#!/usr/bin/env python3
"""Generate procedural sigil splash JPGs for the 12 themes that never
had painted splash art (U-013). Each splash is a tarot-card emblem:
theme palette gradient + radial glow + a hand-drawn geometric sigil +
the theme name in its curated bundled font + film grain + vignette.

Output: gungeon_mate/assets/images/themes/splash/<slug>.jpg (1200x1200,
matching the existing splash set). Re-run any time; overwrite freely.
Real painted art can replace these files later without code changes.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'gungeon_mate', 'assets', 'fonts')
OUT = os.path.join(ROOT, 'gungeon_mate', 'assets', 'images', 'themes', 'splash')
SIZE = 1200


def hx(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def base_gradient(scaffold, card):
    """Vertical gradient scaffold(top) -> card(bottom), slight center lift."""
    img = Image.new('RGB', (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        row = lerp(scaffold, card, t)
        for x in range(SIZE):
            lift = 1.0 + 0.06 * math.sin(math.pi * x / SIZE) * math.sin(math.pi * y / SIZE)
            px[x, y] = tuple(min(255, int(c * lift)) for c in row)
    return img


def radial_glow(img, color, cx, cy, radius, alpha=90):
    layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(alpha * (1 - i / steps) ** 1.6)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.18))
    img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'), (0, 0))


def sigil_cultist(d, x, y, col, acc):
    # Halo ring + candle flame triangle.
    d.ellipse([x - 90, y - 90, x + 90, y + 90], outline=acc + (220,), width=6)
    d.polygon([(x, y - 210), (x + 46, y - 40), (x - 46, y - 40)], fill=col + (235,))
    d.rectangle([x - 16, y - 30, x + 16, y + 150], fill=col + (200,))
    d.line([(x - 60, y + 150), (x + 60, y + 150)], fill=col + (200,), width=10)


def sigil_gunslinger(d, x, y, col, acc):
    # Marshal badge: ring + 6 spokes + center.
    d.ellipse([x - 170, y - 170, x + 170, y + 170], outline=col + (230,), width=10)
    d.ellipse([x - 60, y - 60, x + 60, y + 60], outline=acc + (230,), width=8)
    for i in range(6):
        a = i * math.pi / 3
        x1, y1 = x + 70 * math.cos(a), y + 70 * math.sin(a)
        x2, y2 = x + 165 * math.cos(a), y + 165 * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=acc + (230,), width=12)
    d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=acc + (245,))


def sigil_convict(d, x, y, col, acc):
    # Cell door: ring + vertical bars.
    d.ellipse([x - 160, y - 160, x + 160, y + 160], outline=col + (230,), width=8)
    for i in range(-2, 3):
        bx = x + i * 52
        d.line([(bx, y - 140), (bx, y + 140)], fill=acc + (235,), width=16)
    d.line([(x - 160, y), (x + 160, y)], fill=acc + (235,), width=16)


def sigil_hunter(d, x, y, col, acc):
    # Crosshair + antler ticks.
    d.ellipse([x - 150, y - 150, x + 150, y + 150], outline=col + (230,), width=8)
    d.line([(x - 200, y), (x + 200, y)], fill=acc + (220,), width=8)
    d.line([(x, y - 200), (x, y + 200)], fill=acc + (220,), width=8)
    d.ellipse([x - 55, y - 55, x + 55, y + 55], outline=acc + (245,), width=8)
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        d.line([(x + dx * 60, y + dy * 60), (x + dx * 150, y + dy * 150)],
               fill=col + (230,), width=14)


def sigil_pilot(d, x, y, col, acc):
    # Wing chevrons.
    for k in range(3):
        cy = y - 40 - k * 110
        spread = 300 - k * 45
        col_k = col if k == 0 else acc
        d.line([(x - spread, cy), (x, cy - 55), (x + spread, cy)],
               fill=col_k + (235 - k * 45,), width=14 - k * 3)
    d.ellipse([x - 60, y - 380, x + 60, y - 260], outline=acc + (240,), width=8)


def sigil_rat(d, x, y, col, acc):
    # Cheese wedge with holes.
    d.polygon([(x - 200, y + 90), (x + 200, y + 90), (x + 40, y - 170)],
              fill=col + (200,))
    d.line([(x - 200, y + 90), (x + 200, y + 90)], fill=acc + (230,), width=12)
    for hx_, hy_, hr in [(x - 60, y - 10, 22), (x + 30, y + 20, 30), (x + 110, y - 30, 18)]:
        d.ellipse([hx_ - hr, hy_ - hr, hx_ + hr, hy_ + hr],
                  fill=(20, 16, 10, 200))


def sigil_breach(d, x, y, col, acc):
    # Portal: double ring + slitted rift.
    d.ellipse([x - 180, y - 180, x + 180, y + 180], outline=col + (220,), width=8)
    d.ellipse([x - 120, y - 120, x + 120, y + 120], outline=acc + (235,), width=6)
    for i in range(-3, 4):
        ly = y + i * 34
        d.line([(x - 110, ly), (x + 110, ly)], fill=col + (140,), width=4)
    d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=acc + (235,))


def sigil_leadlord(d, x, y, col, acc):
    # Crown.
    pts = [(x - 190, y + 90), (x - 190, y - 60), (x - 142, y + 10),
           (x - 95, y - 160), (x - 47, y + 10), (x, y - 90),
           (x + 47, y + 10), (x + 95, y - 160), (x + 142, y + 10),
           (x + 190, y - 60), (x + 190, y + 90)]
    d.polygon(pts, fill=col + (215,))
    d.rectangle([x - 190, y + 90, x + 190, y + 130], fill=acc + (220,))
    for jx in (x - 95, x, x + 95):
        d.ellipse([jx - 14, y + 45, jx + 14, y + 73], fill=acc + (240,))


def sigil_oubliette(d, x, y, col, acc):
    # Hanging chain + cell bars.
    for i in range(4):
        cy = y - 220 + i * 110
        d.ellipse([x - 40, cy - 34, x + 40, cy + 34], outline=acc + (230,), width=10)
        d.ellipse([x - 40, cy + 76, x + 40, cy + 144], outline=col + (230,), width=10)
    for i in range(-2, 3):
        bx = x - 140 + i * 70
        d.line([(bx, y + 40), (bx, y + 220)], fill=col + (200,), width=14)


def sigil_blackpowder(d, x, y, col, acc):
    # Bursting powder charge.
    for i in range(12):
        a = i * math.pi / 6
        r1, r2 = 120, 260 if i % 2 == 0 else 200
        d.line([(x + r1 * math.cos(a), y + r1 * math.sin(a)),
                (x + r2 * math.cos(a), y + r2 * math.sin(a))],
               fill=acc + (220,), width=10)
    d.ellipse([x - 110, y - 110, x + 110, y + 110], outline=col + (235,), width=10)
    d.ellipse([x - 50, y - 50, x + 50, y + 50], fill=col + (220,))


def sigil_bullethell(d, x, y, col, acc):
    # Bullet rain - angled streaks + one big round.
    rng = random.Random(7)
    for i in range(40):
        sx = x - 320 + rng.randint(0, 640)
        sy = y - 320 + rng.randint(0, 640)
        ln = rng.randint(30, 90)
        d.line([(sx, sy), (sx - ln * 0.35, sy + ln)],
               fill=acc + (rng.randint(120, 220),), width=5)
    d.ellipse([x - 130, y - 130, x + 130, y + 130], outline=col + (240,), width=12)
    d.ellipse([x - 45, y - 45, x + 45, y + 45], fill=col + (240,))


def sigil_rgdept(d, x, y, col, acc):
    # Shield badge + star.
    shield = [(x, y - 190), (x + 160, y - 130), (x + 160, y + 30),
              (x, y + 210), (x - 160, y + 30), (x - 160, y - 130)]
    d.polygon(shield, outline=col + (235,), width=10)
    star = []
    for i in range(10):
        r = 90 if i % 2 == 0 else 40
        a = -math.pi / 2 + i * math.pi / 5
        star.append((x + r * math.cos(a), y - 10 + r * math.sin(a)))
    d.polygon(star, fill=acc + (240,))


SIGILS = {
    'the_cultist': sigil_cultist,
    'the_gunslinger': sigil_gunslinger,
    'the_convict': sigil_convict,
    'the_hunter': sigil_hunter,
    'the_pilot': sigil_pilot,
    'the_rat': sigil_rat,
    'the_breach': sigil_breach,
    'lead_lord_keep': sigil_leadlord,
    'the_oubliette': sigil_oubliette,
    'black_powder_mine': sigil_blackpowder,
    'bullet_hell': sigil_bullethell,
    'rg_department': sigil_rgdept,
}

# slug, label, scaffold, card, primary, secondary, headline, font file
THEMES = [
    ('the_cultist', 'THE CULTIST', '#0D0F1A', '#161A2E', '#FFD700', '#7B68EE', '#FFE082', 'GoogleFonts.GermaniaOne.ttf'),
    ('the_gunslinger', 'THE GUNSLINGER', '#1A1208', '#2A1E10', '#FFB300', '#FF6F00', '#FFD54F', 'GoogleFonts.GermaniaOne.ttf'),
    ('the_convict', 'THE CONVICT', '#1A0F0A', '#2A1810', '#FF5722', '#D32F2F', '#FF8A65', 'GoogleFonts.Anton.ttf'),
    ('the_hunter', 'THE HUNTER', '#0A1208', '#121E10', '#66BB6A', '#A1887F', '#A5D6A7', 'GoogleFonts.FjallaOne.ttf'),
    ('the_pilot', 'THE PILOT', '#0A0E1A', '#121829', '#42A5F5', '#B0BEC5', '#82B1FF', 'GoogleFonts.FjallaOne.ttf'),
    ('the_rat', 'THE RESOURCEFUL RAT', '#12100A', '#1E1A10', '#FFC107', '#8D6E63', '#FFD54F', 'GoogleFonts.PressStart2P.ttf'),
    ('the_breach', 'THE BREACH', '#0A0814', '#14102A', '#7C4DFF', '#18FFFF', '#B388FF', 'GoogleFonts.FjallaOne.ttf'),
    ('lead_lord_keep', "LEAD LORD'S KEEP", '#12100A', '#221E14', '#C5A05E', '#D4AF37', '#FFD700', 'GoogleFonts.GermaniaOne.ttf'),
    ('the_oubliette', 'THE OUBLIETTE', '#0A1208', '#121E0E', '#8BC34A', '#BF360C', '#AED581', 'GoogleFonts.FjallaOne.ttf'),
    ('black_powder_mine', 'BLACK POWDER MINE', '#0A0A08', '#14140E', '#FF6F00', '#795548', '#FFAB40', 'GoogleFonts.Wallpoet.ttf'),
    ('bullet_hell', 'BULLET HELL', '#0A0404', '#140808', '#D32F2F', '#FFC107', '#FF5252', 'GoogleFonts.Anton.ttf'),
    ('rg_department', 'R&G DEPARTMENT', '#0C0C0C', '#181818', '#00E676', '#E0E0E0', '#69F0AE', 'GoogleFonts.FjallaOne.ttf'),
]


def letterspaced(draw, text, font, xy, fill, spacing, anchor='mm'):
    # Measure total width with spacing.
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x, y = xy
    if anchor == 'mm':
        x -= total / 2
        y -= draw.textbbox((0, 0), 'Ag', font=font)[3] / 2
    elif anchor == 'ms':
        x -= total / 2
    cur = x
    for ch, w in zip(text, widths):
        draw.text((cur, y), ch, font=font, fill=fill)
        cur += w + spacing
    return total


def make_splash(theme):
    slug, label, sc, cd, pr, se, hl, fontfile = theme
    scaffold, card = hx(sc), hx(cd)
    primary, secondary, headline = hx(pr), hx(se), hx(hl)

    img = base_gradient(scaffold, card)
    # Convert once to RGBA for glow/sigil compositing.
    rgba = img.convert('RGBA')

    glow_layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for i in range(30, 0, -1):
        r = 460 * i / 30
        a = int(80 * (1 - i / 30) ** 1.5)
        gd.ellipse([SIZE / 2 - r, 470 - r, SIZE / 2 + r, 470 + r],
                   fill=primary + (a,))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(60))
    rgba = Image.alpha_composite(rgba, glow_layer)

    # Sigil on transparent layer.
    sig = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sig)
    fn = SIGILS[slug]
    # rat sigil needs card color for holes — bind via closure hack
    global card_col
    card_col = card
    fn(sd, SIZE // 2, 470, primary, secondary)
    sig = sig.filter(ImageFilter.GaussianBlur(1.2))
    rgba = Image.alpha_composite(rgba, sig)

    # Name plate.
    nd = ImageDraw.Draw(rgba)
    font = ImageFont.truetype(os.path.join(FONTS, fontfile), 92)
    # Soft shadow pass.
    letterspaced(nd, label, font, (SIZE / 2 + 3, 900 + 3), (0, 0, 0, 160), 10)
    letterspaced(nd, label, font, (SIZE / 2, 900), headline + (255,), 10)

    # Hairline rule under the name.
    nd.line([(SIZE / 2 - 260, 990), (SIZE / 2 + 260, 990)], fill=primary + (180,), width=3)

    # Film grain.
    rng = random.Random(hash(slug) & 0xFFFF)
    noise = Image.effect_noise((SIZE, SIZE), 18).convert('L')
    grain = Image.merge('RGBA', (noise, noise, noise, Image.new('L', (SIZE, SIZE), 26)))
    rgba = Image.alpha_composite(rgba, grain)

    # Vignette.
    vig = Image.new('L', (SIZE, SIZE), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-260, -260, SIZE + 260, SIZE + 260], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    black = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 110))
    rgba = Image.composite(rgba, Image.alpha_composite(rgba, black), vig)

    out = rgba.convert('RGB')
    path = os.path.join(OUT, f'{slug}.jpg')
    out.save(path, 'JPEG', quality=88)
    print('wrote', path)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for t in THEMES:
        make_splash(t)
