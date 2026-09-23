"""
Sitenin alan adını tek yerden değiştirir.

Kullanım:  python tools/set_domain.py https://dosify.com.tr/
Yaptıkları: index.html (canonical, og/twitter, JSON-LD), robots.txt ve tools/build_pages.py içindeki
adresi günceller, ardından alt sayfaları ve site haritasını yeniden üretir.
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "https://dosify-web.onrender.com/"


def replace_in(path, old, new):
    full = os.path.join(ROOT, path)
    s = io.open(full, encoding="utf-8").read()
    n = s.count(old)
    if n:
        io.open(full, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    return n


def main():
    if len(sys.argv) != 2:
        sys.exit("Kullanım: python tools/set_domain.py https://yenialanadi.com.tr/")
    new = sys.argv[1]
    if not new.startswith("https://") or not new.endswith("/"):
        sys.exit("Adres https:// ile başlamalı ve / ile bitmeli. Örnek: https://dosify.com.tr/")

    current = re.search(r'SITE = "([^"]+)"', io.open(os.path.join(ROOT, "tools/build_pages.py"), encoding="utf-8").read()).group(1)
    total = 0
    for path in ("index.html", "robots.txt", "tools/build_pages.py"):
        total += replace_in(path, current, new)
        if current != OLD:
            total += replace_in(path, OLD, new)
    print(f"{current} -> {new} · {total} yerde güncellendi")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_pages.py")], check=True)


if __name__ == "__main__":
    main()
