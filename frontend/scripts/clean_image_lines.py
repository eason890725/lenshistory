"""Remove thin horizontal line artifacts from black-background product images.

The artifacts are light bands left over from screenshot borders when the original
white backgrounds were converted to black. They run almost edge to edge, while the
product sits in the middle. So:

1. A pixel is a line candidate when it sits in a long bright horizontal run AND there
   is pure background black within a few rows above and below. Converted
   backgrounds are ~0 while product blacks sit around 20-40.
2. Only rows whose candidates reach into the left/right edge zones count as line
   rows. That keeps ribs, lettering and thin parts in the middle of the product safe.

Usage: python scripts/clean_image_lines.py <image-or-dir> [...]   (edits in place)
       python scripts/clean_image_lines.py --selftest
"""
import sys
from PIL import Image

BRIGHT = 45      # luminance above which a pixel can belong to a line
PURE = 6         # luminance at or below which a pixel is converted background
MIN_RUN = 30     # shortest horizontal run (px) treated as a line
REACH = 10       # how far above/below (px) to look for background; > line thickness
EDGE = 0.12      # width fraction on each side where real lines show up
EDGE_MIN = 0.04  # candidates needed inside the edge zones, as a fraction of width


def line_candidates(lum, w, h, y):
    out = []
    x = 0
    while x < w:
        if lum[x, y] <= BRIGHT:
            x += 1
            continue
        start = x
        while x < w and lum[x, y] > BRIGHT:
            x += 1
        if x - start < MIN_RUN:
            continue
        for xi in range(start, x):
            above = any(lum[xi, yy] <= PURE for yy in range(max(0, y - REACH), y))
            below = any(lum[xi, yy] <= PURE for yy in range(y + 1, min(h, y + REACH + 1)))
            if above and below:
                out.append(xi)
    return out


def clean(path):
    im = Image.open(path).convert("RGB")
    lum = im.convert("L").load()
    px = im.load()
    w, h = im.size
    left, right = w * EDGE, w * (1 - EDGE)
    changed = 0
    for y in range(h):
        xs = line_candidates(lum, w, h, y)
        if sum(1 for x in xs if x < left or x > right) < w * EDGE_MIN:
            continue
        for x in xs:
            px[x, y] = (0, 0, 0)
        changed += len(xs)
    if changed:
        im.save(path, quality=92)
    return changed


def selftest():
    import os, tempfile
    from PIL import ImageDraw
    im = Image.new("RGB", (450, 450), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 117, 430, 121], fill=(210, 215, 230))    # artifact line, edge to edge
    d.rectangle([150, 150, 300, 300], fill=(30, 30, 30))      # black product body
    d.rectangle([160, 220, 290, 221], fill=(200, 200, 200))   # thin highlight on the body
    d.rectangle([100, 330, 350, 380], fill=(190, 190, 190))   # thick silver part
    d.rectangle([150, 410, 300, 411], fill=(200, 200, 200))   # thin product part on pure black, centred
    path = os.path.join(tempfile.mkdtemp(), "t.png")
    im.save(path)
    clean(path)
    out = Image.open(path).convert("L").load()
    assert out[60, 119] < 10, "artifact line should be removed"
    assert out[200, 220] > 150, "highlight on the product must stay"
    assert out[200, 355] > 150, "thick silver part must stay"
    assert out[200, 410] > 150, "thin part away from the edges must stay"
    print("selftest ok")


if __name__ == "__main__":
    from pathlib import Path
    if sys.argv[1:] == ["--selftest"]:
        selftest()
        sys.exit()
    for arg in sys.argv[1:]:
        paths = sorted(Path(arg).rglob("*.jpg")) if Path(arg).is_dir() else [Path(arg)]
        for p in paths:
            print(f"{clean(p):6d} px  {p}")
