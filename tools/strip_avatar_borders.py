# Strip baked-in frame borders from avatar webp files.
# Frame = rectangular ring of near-uniform color (white/gray/tinted) possibly
# surrounded by a dark margin. We locate the ring per side, crop to its
# interior, and resize back to 320x320.
from PIL import Image
import os, sys

SRC = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SRC, '..', 'gungeon_mate', 'assets', 'images', 'avatars')
SRC = os.path.normpath(SRC)
DRY = '--dry' in sys.argv
OUT_PREVIEW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'avatar_preview')

def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

def line_dom(pix):
    """Return (dominant_color, coverage, dom_lum) for a list of RGB pixels."""
    n = len(pix)
    med = tuple(sorted(p[i] for p in pix)[n // 2] for i in range(3))
    cov = sum(1 for p in pix
              if abs(p[0] - med[0]) + abs(p[1] - med[1]) + abs(p[2] - med[2]) < 90) / n
    return med, cov, lum(med)

def is_bar(pix):
    _, cov, l = line_dom(pix)
    return cov >= 0.75 and l > 50

def is_bar_loose(pix):
    """Fallback for gradient frames: mostly non-dark pixels."""
    n = len(pix)
    return sum(1 for p in pix if lum(p) > 50) / n >= 0.78

def find_bar(getline, n, cap):
    """Scan lines 0..n-1; return (start,end) inclusive of first bar run, or None."""
    for test in (is_bar, is_bar_loose):
        i = 0
        while i < n and not test(getline(i)):
            i += 1
        if i < n:
            j = i
            while j + 1 < n and test(getline(j + 1)) and (j + 1 - i) < cap:
                j += 1
            return i, j
    return None

def process(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    px = im.load()
    cap = max(3, int(w * 0.07))
    row = lambda y: [px[x, y] for x in range(w)]
    col = lambda x: [px[x, y] for y in range(h)]
    top = find_bar(row, h, cap)
    bot_desc = find_bar(lambda k: row(h - 1 - k), h, cap)
    left = find_bar(col, w, cap)
    right_desc = find_bar(lambda k: col(w - 1 - k), w, cap)
    if None in (top, bot_desc, left, right_desc):
        return None
    t0, t1 = top
    b1, b0 = h - 1 - bot_desc[0], h - 1 - bot_desc[1]
    l0, l1 = left
    r1, r0 = w - 1 - right_desc[0], w - 1 - right_desc[1]
    # inset 1-2px inside the ring to drop antialiased edge residue
    ins = 2 if w >= 200 else 1
    box = (l1 + 1 + ins, t1 + 1 + ins, r0 - ins, b0 - ins)
    if box[2] - box[0] < w * 0.5 or box[3] - box[1] < h * 0.5:
        return ('BADBOX', box, (t0, t1, b0, b1, l0, l1, r0, r1))
    return ('OK', box, (t0, t1, b0, b1, l0, l1, r0, r1))

results = {}
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.webp'):
        continue
    r = process(os.path.join(SRC, f))
    results[f] = r
    if r is None:
        print(f, 'NO-FRAME')
    else:
        print(f, r[0], 'crop', r[1], 'bars(t0,t1,b0,b1,l0,l1,r0,r1)', r[2])

APPLY = '--apply' in sys.argv
if not DRY:
    dst_dir = SRC if APPLY else OUT_PREVIEW
    if not APPLY:
        os.makedirs(OUT_PREVIEW, exist_ok=True)
    n = 0
    for f, r in results.items():
        if not r or r[0] != 'OK':
            continue
        im = Image.open(os.path.join(SRC, f)).convert('RGB')
        im.crop(r[1]).resize((320, 320), Image.LANCZOS).save(
            os.path.join(dst_dir, f), quality=95)
        n += 1
    print(('applied to' if APPLY else 'previews written to'), dst_dir, n, 'files')
