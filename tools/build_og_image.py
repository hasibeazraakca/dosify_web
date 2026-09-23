"""
Paylaşım görselini (og-image.png) üretir — WhatsApp/X/LinkedIn'de bağlantı paylaşılınca görünen kart.

Kullanım:  python tools/build_og_image.py [kaynak-logo.png]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(
    os.path.dirname(ROOT), "Dosify_mobile_frontend_1_1", "assets", "dozunda-logo.png"
)

SIZE = (1200, 630)
TOP, BOTTOM = (0, 122, 133), (12, 76, 84)
TITLE = "Dozunda"
SLOGAN = "Her şey dozunda güzel"
LINES = ["İlaç etkileşimi · İlaç hatırlatıcı", "Yakın takibi · Nöbetçi eczane"]


def rounded(size, radius, color):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=color)
    return img


def main():
    src = Image.open(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC).convert("RGBA")
    w, h = src.size
    shield = src.crop((0, 0, w, int(h * 0.72)))
    shield = shield.crop(shield.split()[3].getbbox())

    canvas = Image.new("RGB", SIZE, TOP)
    draw = ImageDraw.Draw(canvas)
    for y in range(SIZE[1]):
        t = y / (SIZE[1] - 1)
        draw.line([(0, y), (SIZE[0], y)], fill=tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3)))

    badge = rounded((220, 220), 48, (255, 255, 255, 255))
    mark = shield.copy()
    mark.thumbnail((152, 152), Image.LANCZOS)
    badge.alpha_composite(mark, ((220 - mark.size[0]) // 2, (220 - mark.size[1]) // 2))
    canvas.paste(badge, (90, 205), badge)

    bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 96)
    regular = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 44)
    small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 33)

    draw = ImageDraw.Draw(canvas)
    draw.text((362, 182), TITLE, font=bold, fill=(255, 255, 255))
    draw.text((364, 292), SLOGAN, font=regular, fill=(214, 240, 240))
    for i, line in enumerate(LINES):
        draw.text((364, 372 + i * 48), line, font=small, fill=(196, 230, 232))

    out = os.path.join(ROOT, "og-image.png")
    canvas.save(out, quality=95)
    print("og-image.png", os.path.getsize(out), "bayt")


if __name__ == "__main__":
    main()
