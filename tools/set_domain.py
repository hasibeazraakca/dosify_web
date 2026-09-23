"""
Sitenin alan adını tek yerden değiştirir.

Kullanım:  python tools/set_domain.py https://dozunda.com/
Yaptıkları: index.html (canonical, og/twitter, JSON-LD), robots.txt ve tools/build_pages.py içindeki
adresi günceller, ardından alt sayfaları ve site haritasını yeniden üretir.
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def replace_in(path, old, new):
    full = os.path.join(ROOT, path)
    s = io.open(full, encoding="utf-8").read()
    n = s.count(old)
    if n:
        io.open(full, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    return n


def main():
    if len(sys.argv) != 2:
        sys.exit("Kullanım: python tools/set_domain.py https://yenialanadi.com/")
    new = sys.argv[1]
    if not new.startswith("https://") or not new.endswith("/"):
        sys.exit("Adres https:// ile başlamalı ve / ile bitmeli. Örnek: https://dozunda.com/")

    build = io.open(os.path.join(ROOT, "tools/build_pages.py"), encoding="utf-8").read()
    current = re.search(r'SITE = "([^"]+)"', build).group(1)
    total = 0
    for path in ("index.html", "robots.txt", "tools/build_pages.py"):
        total += replace_in(path, current, new)
    print(f"{current} -> {new} · {total} yerde güncellendi")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_pages.py")], check=True)


if __name__ == "__main__":
    main()
