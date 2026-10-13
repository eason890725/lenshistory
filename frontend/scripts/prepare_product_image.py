"""Turn a product photo into the site's standard catalogue image.

- White or transparent studio backgrounds are kept white (the site multiplies images onto a tinted plate,
  so white disappears into it).
- Legacy black-background images, and flat light-grey / tinted backdrops, are converted: backdrop pixels
  connected to the border become white.
- The product is trimmed to its bounding box, centred on a square canvas with even padding, and saved
  as WebP (max 1000 px).

Usage: python scripts/prepare_product_image.py <input> <output.webp>
       python scripts/prepare_product_image.py --selftest
"""
import io
import sys
from collections import deque
from PIL import Image, ImageChops, ImageCms, ImageFilter

SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))

SIZE = 1000
PAD = 0.08          # padding on each side, as a fraction of the canvas
DARK_BG = 12        # luminance at or below this, touching the border, counts as black background
WHITE_BG = 245      # luminance at or above this counts as white background when trimming
MIN_SIDE = 500      # products smaller than this in the source get blurry when enlarged to the canvas; refuse them
TINT_TOL = 14       # per-channel distance from a flat light backdrop colour that still counts as backdrop
SHADOW_MIN = 0.5    # a drop shadow at least this bright (relative to the backdrop) is neutralised
SHADOW_CHROMA = 0.025  # max spread of per-channel ratios to the backdrop for a pixel to count as its shadow


def to_srgb(im):
    """Apply an embedded ICC profile (press CMYK JPEGs, Adobe RGB) instead of Pillow's naive conversion,
    which crushes blacks and shifts colours toward magenta."""
    icc = im.info.get("icc_profile")
    if icc and im.mode in ("RGB", "CMYK"):
        try:
            return ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")
        except (ImageCms.PyCMSError, OSError):
            pass
    return im


def flatten(im):
    """RGBA/LA/P → RGB on white."""
    im = to_srgb(im)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def flood_to_white(im, is_bg, paint=lambda p: (255, 255, 255)):
    """Flood-fill background pixels (is_bg(rgb) true) connected to the border and repaint them (white by default)."""
    w, h = im.size
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
        if seen[i] or not is_bg(px[x, y]):
            continue
        seen[i] = 1
        px[x, y] = paint(px[x, y])
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


def border_tint(im):
    """Colour of a flat light non-white backdrop (e.g. Fujifilm AU's mint grey), or None."""
    w, h = im.size
    px = im.load()
    edge = [px[x, y] for x in range(0, w, 4) for y in (0, h - 1)] + [px[x, y] for y in range(0, h, 4) for x in (0, w - 1)]
    bg = tuple(sorted(p[i] for p in edge)[len(edge) // 2] for i in range(3))
    if not 170 <= min(bg) < WHITE_BG:
        return None
    near = sum(max(abs(p[i] - bg[i]) for i in range(3)) <= TINT_TOL for p in edge)
    return bg if near / len(edge) > 0.9 else None


def tint_to_white(tint):
    """Backdrop pixels become white; its soft drop shadow (a darker shade of the same tint) becomes a
    neutral grey of the same relative darkness, so no tinted, hard-edged blob is left under the product.
    Neutral product greys and silvers don't share the backdrop's slight colour cast, so they are kept."""
    def ratio(p):
        return [p[i] / max(1, tint[i]) for i in range(3)]

    def is_bg(p):
        k = ratio(p)
        return max(abs(p[i] - tint[i]) for i in range(3)) <= TINT_TOL or (min(k) >= SHADOW_MIN and max(k) - min(k) <= SHADOW_CHROMA)

    def paint(p):
        if max(abs(p[i] - tint[i]) for i in range(3)) <= TINT_TOL:
            return (255, 255, 255)
        v = min(255, round(255 * sum(ratio(p)) / 3))
        return (v, v, v)
    return is_bg, paint


def prepare(src, dst):
    im = flatten(Image.open(src))
    # Work at most at 2x the output size; the masks below are slow on 5000 px press images
    f = max(1.0, max(im.size) / (2 * SIZE))
    if f > 1:
        im = im.resize((round(im.width / f), round(im.height / f)), Image.LANCZOS)
    if border_is_dark(im):
        im = flood_to_white(im, lambda p: p[0] * 299 + p[1] * 587 + p[2] * 114 <= DARK_BG * 1000)
    elif tint := border_tint(im):
        im = flood_to_white(im, *tint_to_white(tint))
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
    # flat mint-grey backdrop (Fujifilm AU store shots) becomes white, the product stays
    im = Image.new("RGB", (1600, 1200), (223, 233, 230))
    ImageDraw.Draw(im).rectangle([400, 300, 1200, 900], fill=(25, 25, 25))
    im.save(os.path.join(d, "t.png"))
    assert prepare(os.path.join(d, "t.png"), os.path.join(d, "t.webp"))
    out = Image.open(os.path.join(d, "t.webp")).convert("RGB")
    assert max(out.getpixel((SIZE // 2 - 380, SIZE // 2))) < 60, "backdrop should be trimmed so the product fills the frame"
    b = out.tobytes()
    mint = sum(1 for i in range(0, len(b), 3) if max(abs(b[i] - 223), abs(b[i + 1] - 233), abs(b[i + 2] - 230)) <= 6)
    assert mint == 0, f"{mint} backdrop-coloured pixels left"
    # its soft drop shadow turns neutral grey; a silver part touching the backdrop is left alone
    im = Image.new("RGB", (1600, 1200), (223, 233, 230))
    dr = ImageDraw.Draw(im)
    dr.ellipse([350, 820, 1250, 980], fill=(167, 175, 172))                    # shadow = backdrop x 0.75
    dr.rectangle([400, 300, 1200, 900], fill=(25, 25, 25))
    dr.rectangle([1200, 400, 1300, 600], fill=(190, 190, 190))                 # silver dial poking out
    im.save(os.path.join(d, "s.png"))
    assert prepare(os.path.join(d, "s.png"), os.path.join(d, "s.webp"))
    out = Image.open(os.path.join(d, "s.webp")).convert("RGB")
    sh = max((out.getpixel((x, y)) for x in range(150, 850, 50) for y in range(700, 900, 10)), key=lambda p: p[1] - p[0])
    assert sh[1] - sh[0] <= 3, f"shadow should be neutral grey, got {sh}"
    sil = max((out.getpixel((x, y)) for x in range(850, 905, 5) for y in range(310, 440, 10)), key=lambda p: abs(p[0] - 190))
    assert abs(sil[0] - 190) <= 8, f"silver part should keep its tone, got {sil}"
    # CMYK press image with an embedded profile goes through the profile (needs a CMYK profile on this machine)
    swop = r"C:\Windows\System32\spool\drivers\color\RSWOP.icm"
    if os.path.exists(swop):
        im = Image.new("CMYK", (1600, 1200), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle([400, 300, 1200, 900], fill=(0, 255, 255, 0))   # 100% M + Y = press red
        im.save(os.path.join(d, "k.tif"), icc_profile=open(swop, "rb").read())
        assert prepare(os.path.join(d, "k.tif"), os.path.join(d, "k.webp"))
        r, g, b = Image.open(os.path.join(d, "k.webp")).convert("RGB").getpixel((SIZE // 2, SIZE // 2))
        assert r < 250 and g > 15, f"CMYK should be converted through its profile, got {(r, g, b)}"
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
