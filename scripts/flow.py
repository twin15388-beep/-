# -*- coding: utf-8 -*-
"""Простые блок-схемы (для схем сопровождения, структурных схем)."""
import math
import os

from PIL import Image, ImageDraw

from mockui import FB, FR, font

TXT = "#1B1B1B"
BLUE = "#0F6CBD"
LBLUE = "#E8F1FB"
GREY = "#F2F2F2"
GREEN = "#E7F4E8"
GREENL = "#2E7D32"
ORANGE = "#FDF0E2"
ORANGEL = "#B25508"


class Flow:
    def __init__(self, w, h, bg="#FFFFFF", margin=20):
        self.W, self.H = w, h
        self.img = Image.new("RGB", (w, h), bg)
        self.d = ImageDraw.Draw(self.img)
        self.nodes = {}
        self.margin = margin

    def wrap(self, text, maxw, size=15, bold=False):
        f = font(size, bold)
        lines, cur = [], ""
        for wd in text.split():
            test = (cur + " " + wd).strip()
            if self.d.textlength(test, font=f) <= maxw:
                cur = test
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def block(self, key, x, y, w, h, text, shape="rect", fill=LBLUE, outline=BLUE,
              size=15, bold=True, color=TXT, sub=None):
        """x, y — левый верхний угол."""
        d = self.d
        if shape == "rect":
            d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill,
                                outline=outline, width=2)
            ix, iw = x + 10, w - 20
        elif shape == "term":
            d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill,
                                outline=outline, width=2)
            ix, iw = x + 18, w - 36
        elif shape == "diamond":
            pts = [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)]
            d.polygon(pts, fill=fill, outline=outline)
            d.line(pts + [pts[0]], fill=outline, width=2)
            ix, iw = x + w * 0.22, w * 0.56
        elif shape == "db":
            d.rounded_rectangle([x, y + 14, x + w, y + h], radius=6, fill=fill,
                                outline=outline, width=2)
            d.ellipse([x, y, x + w, y + 28], fill=fill, outline=outline, width=2)
            ix, iw = x + 10, w - 20
        elif shape == "doc":
            pts = [(x, y), (x + w - 25, y), (x + w, y + 25), (x + w, y + h), (x, y + h)]
            d.polygon(pts, fill=fill, outline=outline)
            d.line(pts + [pts[0]], fill=outline, width=2)
            d.line([x + w - 25, y, x + w - 25, y + 25, x + w, y + 25], fill=outline, width=2)
            ix, iw = x + 10, w - 20
        elif shape == "cylinder":
            d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                                outline=outline, width=2)
            ix, iw = x + 10, w - 20
        lines = []
        for i, seg in enumerate(text.split("\n")):
            lines += self.wrap(seg, iw, size, bold)
        lh = int(size * 1.35)
        ty = y + (h - lh * len(lines)) // 2 - 2
        maxw = max(self.d.textlength(l, font=font(size, bold)) for l in lines)
        for i, l in enumerate(lines):
            self.d.text((x + w / 2, ty + i * lh), l, font=font(size, bold),
                        fill=color, anchor="ma")
        if sub:
            pass
        self.nodes[key] = (x, y, w, h, shape)
        return self.nodes[key]

    def _edge_point(self, node, tx, ty):
        x, y, w, h, shape = node
        cx, cy = x + w / 2, y + h / 2
        dx, dy = tx - cx, ty - cy
        if shape == "diamond":
            k = 1.0 / (abs(dx) / (w / 2) + abs(dy) / (h / 2) + 1e-9)
            return cx + dx * k, cy + dy * k
        if dx == 0 and dy == 0:
            return cx, cy
        sx = (w / 2) / abs(dx) if dx else 1e9
        sy = (h / 2) / abs(dy) if dy else 1e9
        s = min(sx, sy)
        return cx + dx * s, cy + dy * s

    def link(self, a, b, label="", color="#4A4A4A", dashed=False, width=2,
             label_side="r", head=True, label_dy=0):
        """Ортогональная связь между блоками (по вертикали/горизонтали)."""
        na, nb = self.nodes[a], self.nodes[b]
        ax, ay = na[0] + na[2] / 2, na[1] + na[3] / 2
        bx, by = nb[0] + nb[2] / 2, nb[1] + nb[3] / 2
        if abs(ay - by) < 4:                       # горизонтальная связь
            p1 = (na[0] + na[2], ay) if bx > ax else (na[0], ay)
            p2 = (nb[0], by) if bx > ax else (nb[0] + nb[2], by)
            pts = [p1, p2]
        elif abs(ax - bx) < 4:                     # вертикальная связь
            p1 = (ax, na[1] + na[3]) if by > ay else (ax, na[1])
            p2 = (bx, nb[1]) if by > ay else (bx, nb[1] + nb[3])
            pts = [p1, p2]
        else:
            down = by > ay
            p1 = (ax, na[1] + na[3]) if down else (ax, na[1])
            p2 = (bx, nb[1]) if down else (bx, nb[1] + nb[3])
            ey = (p1[1] + p2[1]) / 2
            pts = [p1, (ax, ey), (bx, ey), p2]
        for i in range(len(pts) - 1):
            self._line(pts[i], pts[i + 1], color, width, dashed)
        if head:
            self._head(pts[-2], pts[-1], color, width)
        if label:
            f = font(13)
            tw = self.d.textlength(label, font=f)
            if len(pts) == 2:
                lx, ly = (pts[0][0] + pts[1][0]) / 2 + 8, (pts[0][1] + pts[1][1]) / 2 - 9
            else:
                seg = pts[1]
                lx, ly = seg[0] + 8, seg[1] - 19
            ly += label_dy
            self.d.rectangle([lx - 2, ly - 1, lx + tw + 2, ly + 16], fill="#FFFFFF")
            self.d.text((lx, ly), label, font=f, fill="#333333")

    def _line(self, p1, p2, color, width, dashed):
        if not dashed:
            self.d.line([p1, p2], fill=color, width=width)
            return
        x1, y1 = p1
        x2, y2 = p2
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(int(L // 10), 1)
        for i in range(n):
            t0, t1 = i / n, (i + 0.55) / n
            self.d.line([x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                         x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1],
                        fill=color, width=width)

    def _head(self, p1, p2, color, width, size=10):
        a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        self.d.polygon([p2,
                        (p2[0] - size * math.cos(a - 0.42), p2[1] - size * math.sin(a - 0.42)),
                        (p2[0] - size * math.cos(a + 0.42), p2[1] - size * math.sin(a + 0.42))],
                       fill=color)

    def caption(self, x, y, text, size=13, color="#4A4A4A", bold=False, anchor="la"):
        self.d.text((x, y), text, font=font(size, bold), fill=color, anchor=anchor)

    def legend(self, x, y, items, box=16):
        for i, (col, txt) in enumerate(items):
            self.d.rectangle([x, y + i * 26, x + box, y + i * 26 + box], fill=col,
                             outline="#888888")
            self.caption(x + box + 8, y + i * 26 + 1, txt, 13)

    def title(self, text, size=19, sub=None):
        self.caption(self.W / 2, 18, text, size, "#1B1B1B", True, "ma")
        if sub:
            self.caption(self.W / 2, 20 + size + 6, sub, 13, "#5D5D5D", False, "ma")

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.img.save(path, quality=95)
        print("IMG:", path)
        return path
