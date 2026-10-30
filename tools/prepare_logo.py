#!/usr/bin/env python3
"""يجهّز شعار «دواجن الوطنية» محلياً من ملف المصدر.

المصدر: assets/images/alwatania-logo-white.png (أبيض — للخلفيات الداكنة).
المخرجات:
  assets/images/alwatania-logo-white.png  نسخة كما هي (خلفية داكنة)
  assets/images/alwatania-logo.png        نسخة للخلفيات الفاتحة (النص الأبيض يصبح أخضر)

شغّل:  python3 tools/prepare_logo.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "assets", "images")
SRC = os.path.join(IMAGES, "alwatania-logo-white.png")
OUT_GREEN = os.path.join(IMAGES, "alwatania-logo.png")

GREEN = (30, 92, 60)


def trim(im):
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def main():
    src = Image.open(SRC).convert("RGBA")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = sp[x, y]
            if a < 10:
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            op[x, y] = (GREEN + (a,)) if lum > 0.75 else (r, g, b, a)

    src = trim(src)
    out = trim(out)
    src.save(SRC)
    out.save(OUT_GREEN)
    print("saved", SRC, src.size)
    print("saved", OUT_GREEN, out.size)


if __name__ == "__main__":
    main()
