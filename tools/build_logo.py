"""
Başlıktaki Dozunda kalkanını üretir: assets/logo-ink.png (açık tema) ve assets/logo-light.png (koyu tema).

Kullanım:  python tools/build_logo.py [kaynak-logo.png]
Varsayılan kaynak, mobil uygulamanın assets/dozunda-logo.png dosyasıdır.

Neden tek renk: kaynak logonun kenarları yumuşak olduğu için 30 piksellik başlıkta silik görünüyordu.
Kalkanın silüetini eşikleyip düz renge boyuyoruz; küçük boyutta net, koyu zeminde de okunur oluyor.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(
    os.path.dirname(os.path.dirname(ROOT)), "Dosify_mobile_frontend_1_1", "assets", "dozunda-logo.png"
)

TARGET = (176, 200)  # 30x34 CSS pikseline ~6x; retina ekranda net
VARIANTS = {
    "logo-ink.png": (10, 77, 87),      # açık tema: koyu petrol
    "logo-light.png": (126, 216, 224),  # koyu tema: açık turkuaz
}


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    src = Image.open(src_path).convert("RGBA")
    w, h = src.size

    # Logonun üst %72'si kalkan, altı DOZUNDA yazısı.
    shield = src.crop((0, 0, w, int(h * 0.72)))
    shield = shield.crop(shield.split()[3].getbbox())

    big = (shield.size[0] * 4, shield.size[1] * 4)
    mask = shield.split()[3].resize(big, Image.LANCZOS).point(lambda v: 255 if v >= 110 else 0)

    for name, color in VARIANTS.items():
        img = Image.new("RGBA", TARGET, color + (255,))
        img.putalpha(mask.resize(TARGET, Image.LANCZOS))
        out = os.path.join(ROOT, "assets", name)
        img.save(out, optimize=True)
        print(name, os.path.getsize(out), "bayt")


if __name__ == "__main__":
    main()
