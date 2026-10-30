#!/usr/bin/env python3
"""يولّد صورة العرض الرئيسية للمنتج (assets/images/product-offer.png).

عدّل القيم في OFFER ثم شغّل:
    python3 tools/make_product_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "product-offer.png")
LOGO = os.path.join(ROOT, "assets", "images", "alwatania-logo-white.png")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GREEN_DARK = (24, 82, 55)
GREEN = (45, 106, 79)
GREEN_LIGHT = (223, 242, 228)
CREAM = (250, 253, 250)

OFFER = {
    "brand": "دواجن الوطنية",
    "title": "عرض بوكس الدجاج العائلي",
    "items": [
        "10 حبات دجاج كامل طازج — 900 غرام للحبة",
        "5 صحون صدور دجاج — 500 غرام للصحن",
        "كيس أرز بسمتي فاخر — 10 كيلو",
    ],
    "price": "30",
    "currency": "ريال",
    "note": "السعر للعرض كامل",
    "footer": "توصيل مجاني خلال 40 دقيقة",
}

W = H = 1200


def ar(text, font):
    return get_display(arabic_reshaper.reshape(text)), font


def main():
    img = Image.new("RGB", (W, H), GREEN)
    d = ImageDraw.Draw(img)

    # خلفية متدرّجة عمودياً
    for y in range(H):
        t = y / H
        r = int(GREEN[0] + (GREEN_DARK[0] - GREEN[0]) * t)
        g = int(GREEN[1] + (GREEN_DARK[1] - GREEN[1]) * t)
        b = int(GREEN[2] + (GREEN_DARK[2] - GREEN[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # الشعار أعلى الصورة
    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        lw = 460
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        img.paste(logo, ((W - lw) // 2, 70), logo)

    # بطاقة بيضاء
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([80, 380, W - 80, H - 90], radius=48, fill=CREAM + (255,))
    img.paste(card, (0, 0), card)

    title_f = ImageFont.truetype(FONT_BOLD, 66)
    item_f = ImageFont.truetype(FONT_BOLD, 40)
    price_f = ImageFont.truetype(FONT_BOLD, 150)
    cur_f = ImageFont.truetype(FONT_BOLD, 56)
    small_f = ImageFont.truetype(FONT_REG, 34)
    note_f = ImageFont.truetype(FONT_REG, 30)

    def center(text, font, y, fill):
        t, f = ar(text, font)
        w = d.textlength(t, font=f)
        d.text(((W - w) / 2, y), t, font=f, fill=fill)
        return w

    center(OFFER["title"], title_f, 425, GREEN_DARK)

    # خط فاصل
    d.line([(230, 530), (W - 230, 530)], fill=GREEN_LIGHT, width=4)

    # بنود العرض
    y = 575
    for item in OFFER["items"]:
        d.ellipse([165, y + 12, 201, y + 48], fill=GREEN)
        d.line([(172, y + 30), (180, y + 39), (194, y + 21)], fill=(255, 255, 255), width=6)
        t, f = ar(item, item_f)
        d.text((225, y + 8), t, font=f, fill=(30, 40, 34))
        y += 78

    # شارة السعر
    py = 835
    d.rounded_rectangle([230, py, W - 230, py + 175], radius=36, fill=GREEN)
    t, f = ar(OFFER["price"], price_f)
    t2, f2 = ar(OFFER["currency"], cur_f)
    num_w = d.textlength(t, font=f)
    cur_w = d.textlength(t2, font=f2)
    gap = 26
    start = (W - (num_w + gap + cur_w)) / 2
    baseline = py + 118
    d.text((start + cur_w + gap, baseline), t, font=f, fill=(255, 255, 255), anchor="ls")
    d.text((start, baseline), t2, font=f2, fill=(255, 255, 255), anchor="ls")
    center(OFFER["note"], note_f, py + 190, (90, 110, 98))

    # التذييل
    t, f = ar(OFFER["footer"], small_f)
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2, H - 78), t, font=f, fill=(255, 255, 255))

    img.save(OUT)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
