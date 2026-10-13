"""Turn a product photo into the site's standard catalogue image.

- White or transparent studio backgrounds are kept white (the site multiplies images onto a tinted plate,
  so white disappears into it).
- Legacy black-background images are converted: background pixels connected to the border become white.
- The product is trimmed to its bounding box, centred on a square canvas with even padding, and saved
  as WebP (max 1000 px).

Usage: python scripts/prepare_product_image.py <input> <output.webp>
       python scripts/prepare_product_image.py --selftest
"""
import sys
from collections import deque
from PIL import Image, ImageChops, ImageFilter

SIZE = 1000
PAD = 0.08          # padding on each side, as a fraction of the canvas
DARK_BG = 12        # luminance at or below this, touching the border, counts as black background
WHITE_BG = 245      # luminance at or above this counts as white background when trimming
MIN_SIDE = 500      # products smaller than this in the source get blurry when enlarged to the canvas; refuse them


def flatten(im):
    """RGBA/LA/P → RGB on white."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def black_to_white(im):
    """Flood-fill near-black pixels connected to the border and paint them white."""
    w, h = im.size
    lum = im.convert("L").load()
    px = im.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i] or lum[x, y] > DARK_BG:
            continue
        seen[i] = 1
        px[x, y] = (255, 255, 255)
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    return im


def border_is_dark(im):
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    edge = [px[x, y] for x in range(0, w, 4) for y in (0, h - 1)] + [px[x, y] for y in range(0, h, 4) for x in (0, w - 1)]
    return sum(v <= DARK_BG for v in edge) / len(edge) > 0.9


def prepare(src, dst):
    im = flatten(Image.open(src))
    # Work at most at 2x the output size; the masks below are slow on 5000 px press images
    f = max(1.0, max(im.size) / (2 * SIZE))
    if f > 1:
        im = im.resize((round(im.width / f), round(im.height / f)), Image.LANCZOS)
    if border_is_dark(im):
        im = black_to_white(im)
    # Product mask: non-white pixels, with thin specks and leftover line fragments opened away.
    # Anything not within a few px of the cleaned mask is painted white, then we trim to the mask.
    mask = ImageChops.invert(im.convert("L")).point(lambda v: 255 if v > 255 - WHITE_BG else 0)
    k = max(3, (min(im.size) // 150) | 1)
    clean = mask.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    keep = clean.filter(ImageFilter.MaxFilter(k * 2 + 1))
    im = Image.composite(im, Image.new("RGB", im.size, (255, 255, 255)), keep)
    box = clean.getbbox()
    if not box or max(box[2] - box[0], box[3] - box[1]) * f < MIN_SIDE:   # measured in source pixels
        return False
    im = im.crop(box)
    inner = int(SIZE * (1 - 2 * PAD))
    scale = inner / max(im.size)   # fit (enlarges at most SIZE / MIN_SIDE times)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    canvas.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2))
    canvas.save(dst, "WEBP", quality=84, method=6)
    return True


def selftest():
    import os, tempfile
    from PIL import ImageDraw
    d = tempfile.mkdtemp()
    # black background, grey product off-centre
    im = Image.new("RGB", (1600, 800), (0, 0, 0))
    ImageDraw.Draw(im).rectangle([200, 200, 800, 700], fill=(60, 60, 60))
    im.save(os.path.join(d, "a.png"))
    assert prepare(os.path.join(d, "a.png"), os.path.join(d, "a.webp"))
    out = Image.open(os.path.join(d, "a.webp")).convert("L")
    assert out.size == (SIZE, SIZE)
    assert out.getpixel((5, 5)) > 240, "background should be white"
    assert out.getpixel((SIZE // 2, SIZE // 2)) < 90, "product should stay dark and be centred"
    # transparent PNG
    im = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([100, 100, 700, 700], fill=(20, 20, 20, 255))
    im.save(os.path.join(d, "b.png"))
    assert prepare(os.path.join(d, "b.png"), os.path.join(d, "b.webp"))
    out = Image.open(os.path.join(d, "b.webp")).convert("L")
    assert out.getpixel((5, 5)) > 240 and out.getpixel((SIZE // 2, SIZE // 2)) < 60
    # a thumbnail-sized source is refused instead of being blown up into a blurry image
    im = Image.new("RGB", (240, 160), (255, 255, 255))
    ImageDraw.Draw(im).rectangle([20, 20, 220, 140], fill=(20, 20, 20))
    im.save(os.path.join(d, "c.png"))
    assert not prepare(os.path.join(d, "c.png"), os.path.join(d, "c.webp"))
    assert not os.path.exists(os.path.join(d, "c.webp"))
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        prepare(sys.argv[1], sys.argv[2])
