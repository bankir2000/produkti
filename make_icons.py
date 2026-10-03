"""Generate PWA icons (three cartridges on dark green) in the app's night-theme palette."""
from pathlib import Path

from PIL import Image, ImageDraw

BG = (13, 15, 13)
BG_GRAD = (26, 40, 26)
BRASS = (222, 170, 64)
BRASS_DARK = (150, 108, 34)
TIP = (125, 212, 68)
TIP_DARK = (74, 138, 56)
OUT_DIR = Path(__file__).parent / "icons"
SS = 2  # supersampling factor for smooth edges


def draw_cartridge(draw: ImageDraw.ImageDraw, x: float, base_y: float, height: float, unit: float) -> None:
    """Draw one upright cartridge.

    Args:
        draw: Pillow drawing context.
        x: Horizontal center in pixels.
        base_y: Y coordinate of the cartridge bottom.
        height: Total height in design units.
        unit: Pixels per design unit.
    """
    half = 12 * unit
    top = base_y - height * unit
    casing_top = top + height * 0.42 * unit
    # Bullet tip: pointed ogive (ellipse top + straight lower part)
    hw = half * 0.85
    ogive = hw * 1.9
    draw.ellipse([x - hw, top, x + hw, top + 2 * ogive], fill=TIP)
    draw.rectangle([x - hw, top + ogive, x + hw, casing_top + 6 * unit], fill=TIP)
    draw.rectangle([x - hw, casing_top - 2 * unit, x + hw, casing_top + 6 * unit], fill=TIP_DARK)
    # Casing
    draw.rectangle([x - half, casing_top + 6 * unit, x + half, base_y], fill=BRASS)
    # Rim at the base
    draw.rectangle([x - half * 1.15, base_y - 7 * unit, x + half * 1.15, base_y], fill=BRASS_DARK)
    # Highlight stripe
    draw.rectangle([x - half * 0.55, casing_top + 12 * unit, x - half * 0.3, base_y - 12 * unit], fill=(244, 207, 120))


def draw_all(draw: ImageDraw.ImageDraw, size: int, scale: float) -> None:
    """Draw the three-cartridge composition centered on the canvas."""
    unit = size * 0.66 * scale / 100
    base_y = size / 2 + 48 * unit
    for dx, h in ((-30, 78), (0, 96), (30, 78)):
        draw_cartridge(draw, size / 2 + dx * unit, base_y, h, unit)


def render(size: int, scale: float, rounded: bool) -> Image.Image:
    """Render one icon at the given size (scale ~0.78 for maskable icons)."""
    big = size * SS
    img = Image.new("RGBA", (big, big), BG)
    d = ImageDraw.Draw(img)
    for y in range(big):
        t = y / big
        d.line([(0, y), (big, y)], fill=tuple(int(BG[i] + (BG_GRAD[i] - BG[i]) * t) for i in range(3)))
    draw_all(d, big, scale)
    if rounded:
        mask = Image.new("L", (big, big), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.22), fill=255)
        img.putalpha(mask)
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for size in (192, 512):
        render(size, 1.0, rounded=True).save(OUT_DIR / f"icon-{size}.png")
        render(size, 0.78, rounded=False).save(OUT_DIR / f"maskable-{size}.png")
    render(180, 0.9, rounded=False).convert("RGB").save(OUT_DIR / "apple-touch-icon.png")
    render(48, 1.0, rounded=True).save(OUT_DIR / "favicon-48.png")
    render(256, 1.0, rounded=True).save(OUT_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])


if __name__ == "__main__":
    main()
