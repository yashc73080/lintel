"""Renders the Lintel trilithon icon: a beam resting on two posts on a pale teal tile.
Small sizes use chunkier shapes so the beam and posts stay distinct at 16 px."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

TILE = (225, 245, 238, 255)   # teal 50
BEAM = (8, 80, 65, 255)       # teal 800
POST = (15, 110, 86, 255)     # teal 600
SS = 8


def draw(size: int) -> Image.Image:
    n = size * SS
    u = n / 88.0
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4 * u, 4 * u, 84 * u, 84 * u], radius=20 * u, fill=TILE)
    if size < 32:
        d.rounded_rectangle([12 * u, 18 * u, 76 * u, 34 * u], radius=3 * u, fill=BEAM)
        d.rounded_rectangle([18 * u, 37 * u, 36 * u, 72 * u], radius=2 * u, fill=POST)
        d.rounded_rectangle([52 * u, 37 * u, 70 * u, 72 * u], radius=2 * u, fill=POST)
    else:
        d.rounded_rectangle([16 * u, 22 * u, 72 * u, 34 * u], radius=3 * u, fill=BEAM)
        d.rounded_rectangle([22 * u, 36 * u, 34 * u, 68 * u], radius=2 * u, fill=POST)
        d.rounded_rectangle([54 * u, 36 * u, 66 * u, 68 * u], radius=2 * u, fill=POST)
    return img.resize((size, size), Image.LANCZOS)


out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
out.mkdir(parents=True, exist_ok=True)
sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
frames = [draw(s) for s in sizes]
frames[-1].save(out / "icon.ico", sizes=[(s, s) for s in sizes], append_images=frames[:-1])
draw(256).save(out / "icon.png")
