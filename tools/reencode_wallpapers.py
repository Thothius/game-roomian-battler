"""Re-encode custom wallpapers to a sane size/quality budget.

U-014 pipeline: wallpapers ship as lossy WebP. This normalizes them —
cap width, re-encode at a fixed quality — without touching filenames
or the pubspec asset dirs.

Usage (from gungeon_mate/):
    python ../tools/reencode_wallpapers.py            # defaults below
    python ../tools/reencode_wallpapers.py --width 1200 --quality 70

Defaults chosen 2026-11-25: wallpapers render under a ~62% readability
scrim (CustomWallpaper.scrimStrength), so q75 is visually safe; width
cap 1280 covers ~1440px phones at cover-fit without visible softness.
"""

import argparse
import glob
import os

from PIL import Image


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--quality", type=int, default=75)
    ap.add_argument(
        "--dir",
        default="assets/images/wallpapers/custom",
        help="wallpaper directory, relative to gungeon_mate/",
    )
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.webp")))
    if not files:
        raise SystemExit(f"no .webp files in {args.dir}")

    before = after = 0
    capped = 0
    for f in files:
        before += os.path.getsize(f)
        im = Image.open(f)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        w, h = im.size
        if w > args.width:
            im = im.resize((args.width, round(h * args.width / w)), Image.LANCZOS)
            capped += 1
        im.save(f, "WEBP", quality=args.quality, method=6)
        after += os.path.getsize(f)

    print(
        f"{len(files)} files, {capped} width-capped\n"
        f"before: {before / 1e6:.1f} MB   after: {after / 1e6:.1f} MB   "
        f"saved: {(before - after) / 1e6:.1f} MB "
        f"({100 * (before - after) / before:.0f}%)"
    )


if __name__ == "__main__":
    main()
