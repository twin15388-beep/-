# -*- coding: utf-8 -*-
"""Отрисовка реалистичных макетов окон Windows 11 / приложений (для отчётов)."""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

_cache = {}


def font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _cache:
        path = FM if mono else (FB if bold else FR)
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


WHITE = "#FFFFFF"
BG = "#F3F3F3"
CARD = "#FFFFFF"
TXT = "#1B1B1B"
MUTED = "#5D5D5D"
LINE = "#E1E1E1"
ACCENT = "#0F6CBD"
SEL = "#DCE9F7"
HOVER = "#F0F0F0"


def rounded(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def desktop(w, h):
    """Мягкий градиентный «рабочий стол» Windows 11."""
    img = Image.new("RGB", (w, h), "#0B3D6B")
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(10 + 40 * t)
        g = int(48 + 70 * t)
        b = int(96 + 90 * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    # «лепестки» цветка Windows 11
    blob = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    cx, cy = w * 0.5, h * 0.52
    bd.ellipse([cx - w * 0.30, cy - h * 0.34, cx + w * 0.12, cy + h * 0.10],
               fill=(70, 150, 230, 90))
    bd.ellipse([cx - w * 0.06, cy - h * 0.12, cx + w * 0.32, cy + h * 0.30],
               fill=(120, 90, 210, 80))
    blob = blob.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img.convert("RGBA"), blob).convert("RGB")
    return img


class Win:
    """Окно приложения. Координаты содержимого — в пикселях изображения."""

    def __init__(self, w=1250, h=800, title="", tabs=None, accent=ACCENT,
                 margin=16, ribbon=None, status=None, toolbar=None):
        self.W, self.H = w, h
        self.base = desktop(w, h)
        self.img = self.base.convert("RGBA")
        self.d = ImageDraw.Draw(self.img)
        self.accent = accent
        x0, y0 = margin, margin
        x1, y1 = w - margin, h - margin

        # тень окна
        shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([x0 - 4, y0 + 6, x1 + 4, y1 + 10], radius=18,
                             fill=(0, 0, 0, 110))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        self.img = Image.alpha_composite(self.img, shadow)
        self.d = ImageDraw.Draw(self.img)

        self.box = (x0, y0, x1, y1)
        self.d.rounded_rectangle(self.box, radius=12, fill="#FAFAFA",
                                 outline="#C9C9C9", width=1)
        # заголовок окна
        self.title_h = 42
        self.d.rounded_rectangle([x0, y0, x1, y0 + self.title_h + 12], radius=12,
                                 fill="#F3F3F3")
        self.d.rectangle([x0 + 1, y0 + self.title_h, x1 - 1, y0 + self.title_h + 12],
                         fill="#F3F3F3")
        # иконка приложения
        self.app_icon(x0 + 16, y0 + 13)
        self.text(x0 + 42, y0 + 11, title, 15, TXT)
        # кнопки управления окном
        bx = x1 - 14
        self._cap_buttons(bx, y0 + 14)

        self.y = y0 + self.title_h + 1
        if tabs:
            self.tabbar(tabs, x0 + 8, self.y + 6, x1 - 8)
            self.y += 44
        if ribbon:
            self.ribbon(ribbon)
        if toolbar:
            self.toolbar(toolbar, x0 + 14, self.y + 8, x1 - 14)
            self.y += 44
        if status:
            self.statusbar(status)
        self.x0, self.x1 = x0, x1
        self.cy0 = self.y

    # ------------------------------------------------------------------ базовое
    def app_icon(self, x, y):
        d = self.d
        d.rounded_rectangle([x, y, x + 17, y + 17], radius=4, fill=self.accent)
        d.rounded_rectangle([x + 4, y + 4, x + 13, y + 13], radius=2, fill="#FFFFFF")

    def _cap_buttons(self, bx, by):
        d = self.d
        by = by + 4
        d.line([bx - 24, by + 1, bx - 16, by + 1], fill="#3A3A3A", width=1)
        d.rectangle([bx - 2, by - 3, bx + 8, by + 5], outline="#3A3A3A", width=1)
        cx, cy = bx + 26, by + 1
        d.line([cx - 5, cy - 5, cx + 5, cy + 5], fill="#3A3A3A", width=2)
        d.line([cx - 5, cy + 5, cx + 5, cy - 5], fill="#3A3A3A", width=2)
        self._close_rect = (cx - 14, by - 10, cx + 14, by + 10)

    def text(self, x, y, s, size=15, color=TXT, bold=False, mono=False, anchor="la"):
        self.d.text((x, y), s, font=font(size, bold, mono), fill=color, anchor=anchor)

    def fit(self, x, y, s, maxw, size=15, color=TXT, bold=False, mono=False):
        f = font(size, bold, mono)
        if self.d.textlength(s, font=f) <= maxw:
            self.text(x, y, s, size, color, bold, mono)
            return s
        out = s
        while out and self.d.textlength(out + "…", font=f) > maxw:
            out = out[:-1]
        self.text(x, y, out + "…", size, color, bold, mono)
        return out + "…"

    def wrap(self, x, y, s, maxw, size=15, color=TXT, bold=False, lh=None):
        f = font(size, bold)
        lh = lh or int(size * 1.45)
        words, line, yy = s.split(), "", y
        for wd in words:
            test = (line + " " + wd).strip()
            if self.d.textlength(test, font=f) <= maxw:
                line = test
            else:
                self.text(x, yy, line, size, color, bold)
                yy += lh
                line = wd
        if line:
            self.text(x, yy, line, size, color, bold)
            yy += lh
        return yy

    # -------------------------------------------------------------- заголовок
    def tabbar(self, tabs, x, y, x1, active=0):
        cx = x
        self._tab_pos = []
        for i, t in enumerate(tabs):
            w = int(self.d.textlength(t, font=font(14)) + 26)
            if i == active:
                self.d.line([cx + 8, y + 28, cx + w - 8, y + 28], fill=self.accent, width=3)
            self.text(cx + 12, y + 5, t, 14, TXT if i == active else MUTED,
                      bold=(i == active))
            self._tab_pos.append((cx, w))
            cx += w

    def ribbon(self, items):
        x0, x1 = self.box[0], self.box[2]
        top = self.y
        h = 76
        self.d.rectangle([x0 + 1, top, x1 - 1, top + h], fill="#FBFBFB")
        self.d.line([x0 + 1, top + h, x1 - 1, top + h], fill=LINE)
        if isinstance(items, str):
            items = [(items, "")]
        cx = x0 + 16
        for label, sub in items:
            w = int(self.d.textlength(label, font=font(14))) + 22
            self.d.rounded_rectangle([cx, top + 12, cx + w, top + 44], radius=5,
                                     fill="#FFFFFF", outline="#C8C8C8")
            self.text(cx + 11, top + 19, label, 14)
            cx += w + 8
        if items and items[0][1]:
            self.text(x0 + 16, top + 52, items[0][1], 12, MUTED)
        self.y = top + h + 1

    def toolbar(self, items, x, y, x1):
        self.d.rounded_rectangle([x, y, x1, y + 30], radius=5, fill="#FFFFFF",
                                 outline="#D5D5D5")
        cx = x + 10
        self._tb = []
        for it in items:
            w = int(self.d.textlength(it, font=font(14))) + 18
            self.text(cx, y + 6, it, 14, "#1B1B1B")
            self._tb.append((it, cx - 4, w))
            cx += w + 6
            if it != items[-1]:
                self.d.line([cx - 6, y + 6, cx - 6, y + 24], fill="#E5E5E5")

    def statusbar(self, left, right=None):
        x0, x1 = self.box[0], self.box[2]
        y = self.box[3] - 30
        self.d.rectangle([x0 + 1, y, x1 - 1, y + 29], fill="#F3F3F3")
        self.d.line([x0 + 1, y, x1 - 1, y], fill=LINE)
        self.text(x0 + 14, y + 7, left, 13, MUTED)
        if right:
            self.text(x1 - 14, y + 7, right, 13, MUTED, anchor="ra")

    # -------------------------------------------------------------- элементы
    def panel(self, x, y, w, h, fill=CARD, outline=LINE, r=8):
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill,
                                 outline=outline, width=1)

    def sidebar(self, x, y, w, items, active=0, title=None):
        self.d.rectangle([x, y, x + w, self.box[3] - 1], fill="#F7F7F7")
        self.d.line([x + w, y, x + w, self.box[3] - 1], fill=LINE)
        cy = y + 14
        if title:
            self.text(x + 16, cy, title, 12, MUTED, bold=True)
            cy += 24
        for i, it in enumerate(items):
            if i == active:
                self.d.rounded_rectangle([x + 8, cy, x + w - 8, cy + 32], radius=5,
                                         fill=SEL)
            self.fit(x + 18, cy + 7, it, w - 34, 14, TXT, bold=(i == active))
            cy += 34
        return cy

    def row(self, x, y, w, h=34, text="", size=14, color=TXT, bold=False,
            icon=None, selected=False, sub=None):
        if selected:
            self.d.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=SEL)
        if icon:
            self.d.rounded_rectangle([x + 10, y + h // 2 - 7, x + 24, y + h // 2 + 7],
                                     radius=3, fill=icon)
            self.text(x + 32, y + (h - size) // 2 - 1, text, size, color, bold)
        else:
            self.text(x + 10, y + (h - size) // 2 - 1, text, size, color, bold)
        if sub:
            pass

    def keyval(self, x, y, w, key, val, kh=210, size=14):
        self.text(x, y, key, size, MUTED)
        vx = x + kh
        self.text(vx, y, val, size, TXT, bold=True)
        return y + 26

    def field(self, x, y, w, value="", h=30, size=14, mono=False, caret=False):
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill="#FFFFFF",
                                 outline="#B6B6B6")
        self.d.rectangle([x + 1, y + h // 2 - 7, x + 4, y + h // 2 + 7], fill="#B6B6B6")
        self.text(x + 10, y + (h - size) // 2 - 2, value, size, TXT, mono=mono)
        if caret:
            cx = x + 12 + self.d.textlength(value, font=font(size, mono=mono))
            self.d.line([cx, y + 6, cx, y + h - 6], fill="#1B1B1B", width=1)

    def button(self, x, y, w, label, primary=False, h=30, size=14, enabled=True,
               arrow=False):
        if primary:
            self.d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=self.accent)
            col = "#FFFFFF"
        else:
            self.d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill="#FDFDFD",
                                     outline="#C6C6C6")
            col = TXT if enabled else "#9A9A9A"
        self.text(x + w // 2, y + (h - size) // 2 - 1, label, size, col,
                  anchor="ma")
        if arrow:
            self.text(x + w - 14, y + (h - size) // 2 - 1, "v", 11, col, anchor="ma")

    def checkbox(self, x, y, label, checked=True, size=14):
        b = 16
        self.d.rounded_rectangle([x, y + 3, x + b, y + 3 + b], radius=3,
                                 fill="#FFFFFF", outline="#8A8A8A")
        if checked:
            self.d.rounded_rectangle([x, y + 3, x + b, y + 3 + b], radius=3, fill=self.accent)
            self.d.line([x + 4, y + 11, x + 7, y + 14], fill="#FFFFFF", width=2)
            self.d.line([x + 7, y + 14, x + 13, y + 7], fill="#FFFFFF", width=2)
        self.text(x + b + 8, y, label, size, TXT)
        return x + b + 12 + self.d.textlength(label, font=font(size))

    def radio(self, x, y, label, selected=False, size=14, w=None):
        r = 15
        self.d.ellipse([x, y + 4, x + r, y + 4 + r], outline="#8A8A8A", fill="#FFFFFF")
        if selected:
            self.d.ellipse([x + 4, y + 8, x + r - 4, y + 4 + r - 4], fill=self.accent)
        self.text(x + r + 8, y, label, size, TXT)
        return x + r + 10 + self.d.textlength(label, font=font(size))

    def menu(self, x, y, items, width=250, highlight=None, checked=None):
        h = 32
        total = sum(h for it in items if it is not None) + 12
        self.d.rounded_rectangle([x, y, x + width, y + total], radius=6, fill="#FBFBFB",
                                 outline="#C4C4C4")
        cy = y + 6
        for i, it in enumerate(items):
            if it is None:
                self.d.line([x + 10, cy + 3, x + width - 10, cy + 3], fill=LINE)
                cy += 8
                continue
            if highlight is not None and i == highlight:
                self.d.rounded_rectangle([x + 5, cy, x + width - 5, cy + h], radius=4,
                                         fill=SEL)
            self.text(x + 16, cy + 7, it, 14, TXT)
            if checked and i in checked:
                self.text(x + width - 22, cy + 7, "✓", 14, TXT)
            cy += h
        return y + total

    def arrow(self, x1, y1, x2, y2, color="#4A4A4A", width=2, head=8):
        self.d.line([x1, y1, x2, y2], fill=color, width=width)
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        for s in (2.6, -2.6):
            self.d.line([x2, y2, x2 - head * math.cos(a + s / 6.2),
                         y2 - head * math.sin(a + s / 6.2)], fill=color, width=width)

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.img.convert("RGB").save(path, quality=95)
        print("IMG:", path)
        return path


def dialog(title, ww, hh, W=1100, H=760, subtitle=None, icon_color=ACCENT):
    """Отрисовка модального диалогового окна. Возвращает (img, draw, box)."""
    img = desktop(W, H)
    # затемнение фона
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 70))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)
    x, y = (W - ww) // 2, (H - hh) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x - 6, y + 8, x + ww + 6, y + hh + 14],
                                        radius=14, fill=(0, 0, 0, 130))
    from PIL import ImageFilter as _IF
    img = Image.alpha_composite(img, sh.filter(_IF.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + ww, y + hh], radius=10, fill="#F5F5F5",
                        outline="#BFBFBF")
    d.rounded_rectangle([x, y, x + ww, y + 40], radius=10, fill="#EDEDED")
    d.rectangle([x + 1, y + 28, x + ww - 1, y + 40], fill="#EDEDED")
    d.text((x + 14, y + 11), title, font=font(15), fill=TXT)
    cx = x + ww - 26
    d.line([cx - 5, y + 15, cx + 5, y + 25], fill="#3A3A3A", width=2)
    d.line([cx - 5, y + 25, cx + 5, y + 15], fill="#3A3A3A", width=2)
    if subtitle:
        d.text((x + 20, y + 52), subtitle, font=font(14, bold=True), fill=TXT)
    return img, d, (x, y, x + ww, y + hh)


def dialog_buttons(d, box, labels=("ОК", "Отмена"), y=None, primary_first=True):
    x0, y0, x1, y1 = box
    y = y if y is not None else y1 - 52
    bw, gap = 100, 10
    n = len(labels)
    sx = x1 - 20 - n * bw - (n - 1) * gap
    for i, lab in enumerate(labels):
        bx = sx + i * (bw + gap)
        prim = (i == 0 and primary_first)
        if prim:
            d.rounded_rectangle([bx, y, bx + bw, y + 32], radius=4, fill=ACCENT)
            d.text((bx + bw / 2, y + 8), lab, font=font(14), fill="#FFFFFF", anchor="ma")
        else:
            d.rounded_rectangle([bx, y, bx + bw, y + 32], radius=4, fill="#FDFDFD",
                                outline="#C6C6C6")
            d.text((bx + bw / 2, y + 8), lab, font=font(14), fill=TXT, anchor="ma")
    return sx


def text_field(d, x, y, w, value="", h=30, size=14, focused=False, mono=False,
               placeholder=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill="#FFFFFF",
                        outline=ACCENT if focused else "#B0B0B0",
                        width=2 if focused else 1)
    if value:
        d.text((x + 9, y + (h - size) // 2 - 2), value, font=font(size, mono=mono), fill=TXT)
    elif placeholder:
        d.text((x + 9, y + (h - size) // 2 - 2), placeholder, font=font(size),
               fill="#9A9A9A")


def str_list(d, x, y, w, rows, h=26, size=14, sel=None, checkboxes=False,
             checked=None, bold_first=False):
    y0 = y
    d.rectangle([x, y, x + w, y + h * len(rows) + 4], fill="#FFFFFF", outline="#C0C0C0")
    cy = y + 2
    for i, r in enumerate(rows):
        if sel is not None and i == sel:
            d.rectangle([x + 1, cy, x + w - 1, cy + h - 2], fill=SEL)
        tx = x + 8
        if checkboxes:
            d.rectangle([x + 8, cy + 6, x + 21, cy + 19], outline="#8A8A8A", fill="#FFFFFF")
            if checked and i in checked:
                d.rectangle([x + 8, cy + 6, x + 21, cy + 19], fill=ACCENT)
                d.line([x + 11, cy + 13, x + 13, cy + 16], fill="#FFFFFF", width=2)
                d.line([x + 13, cy + 16, x + 18, cy + 9], fill="#FFFFFF", width=2)
            tx = x + 30
        d.text((tx, cy + 4), r, font=font(size, bold=(bold_first and i == 0)), fill=TXT)
        cy += h
    return cy


def win_modal(win, ww, hh, title, dim=True, y_off=0):
    """Модальный диалог поверх уже нарисованного окна."""
    W, H = win.W, win.H
    if dim:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 55))
        win.img = Image.alpha_composite(win.img, ov)
    d = ImageDraw.Draw(win.img)
    x, y = (W - ww) // 2, (H - hh) // 2 + y_off
    from PIL import ImageFilter as _IF
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x - 5, y + 7, x + ww + 5, y + hh + 12],
                                        radius=12, fill=(0, 0, 0, 130))
    win.img = Image.alpha_composite(win.img, sh.filter(_IF.GaussianBlur(10)))
    d = ImageDraw.Draw(win.img)
    d.rounded_rectangle([x, y, x + ww, y + hh], radius=8, fill="#F5F5F5",
                        outline="#BDBDBD")
    d.rounded_rectangle([x, y, x + ww, y + 38], radius=8, fill="#EDEDED")
    d.rectangle([x + 1, y + 26, x + ww - 1, y + 38], fill="#EDEDED")
    d.text((x + 14, y + 10), title, font=font(15), fill=TXT)
    cx = x + ww - 24
    d.line([cx - 5, y + 14, cx + 5, y + 24], fill="#3A3A3A", width=2)
    d.line([cx - 5, y + 24, cx + 5, y + 14], fill="#3A3A3A", width=2)
    win.d = d
    return d, (x, y, x + ww, y + hh)


def mbutton(d, x, y, w, label, primary=False, h=30, size=13):
    """Кнопка в модальном окне (по ImageDraw)."""
    if primary:
        d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=ACCENT)
        col = "#FFFFFF"
    else:
        d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill="#FDFDFD",
                            outline="#C6C6C6")
        col = TXT
    d.text((x + w / 2, y + (h - size) // 2 - 1), label, font=font(size), fill=col,
           anchor="ma")
