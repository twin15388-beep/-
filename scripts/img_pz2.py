# -*- coding: utf-8 -*-
"""Иллюстрации к ПЗ № 1 (МДК 06.02): главное меню, сведения о системе."""
import os

from PIL import Image, ImageDraw

from mockui import (ACCENT, BG, CARD, LINE, MUTED, SEL, TXT, WHITE, Win, desktop,
                    font, rounded)

OUT = "/home/user/-/Выполненные работы/Иллюстрации/ПЗ_1_МДК_06.02_анализ_ПО"
os.makedirs(OUT, exist_ok=True)


def start_menu():
    W, H = 1280, 820
    img = desktop(W, H)
    d = ImageDraw.Draw(img)
    # панель «Пуск»
    pw, ph = 660, 612
    px, py = (W - pw) // 2, (H - ph) // 2 + 40
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([px - 6, py + 10, px + pw + 6, py + ph + 16],
                                        radius=22, fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(16))).convert("RGB")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill="#F9F9F9",
                        outline="#CFCFCF")
    # строка поиска
    d.rounded_rectangle([px + 26, py + 20, px + pw - 168, py + 56], radius=18, fill="#FFFFFF",
                        outline="#C9C9C9")
    d.ellipse([px + 40, py + 30, px + 52, py + 42], outline="#5A5A5A", width=2)
    d.line([px + 51, py + 41, px + 57, py + 47], fill="#5A5A5A", width=2)
    d.text((px + 64, py + 28), "Поиск приложений и документов", font=font(14), fill=MUTED)
    d.text((px + pw - 156, py + 30), "Разин К.Е.", font=font(13), fill=TXT)
    d.ellipse([px + pw - 44, py + 22, px + pw - 14, py + 52], fill=ACCENT)
    d.text((px + pw - 29, py + 30), "РК", font=font(12, bold=True), fill="#FFFFFF", anchor="ma")

    d.text((px + 34, py + 76), "Закреплено", font=font(15, bold=True), fill=TXT)
    d.text((px + pw - 110, py + 76), "Все приложения  >", font=font(12), fill=MUTED)

    apps = [("Word", "#2B579A", "W"), ("Excel", "#217346", "X"), ("PowerPoint", "#B7472A", "P"),
            ("Браузер Edge", "#0F6CBD", "e"), ("Проводник", "#F2B90D", "П"),
            ("Параметры", "#5C6B7A", "*"), ("Калькулятор", "#4A4A4A", "="),
            ("Блокнот", "#3B7ABF", "Б"), ("Paint", "#7A3FA0", "К"),
            ("WinRAR", "#8C2B2B", "R"), ("7-Zip", "#1F6F3F", "7"),
            ("Антивирус", "#1C6E4A", "A"), ("Командная строка", "#2B2B2B", ">_"),
            ("Диспетчер задач", "#0A6E9E", "Д"), ("Ножницы", "#B03A5B", "Н"),
            ("Сведения о системе", "#0F6CBD", "i"), ("Adobe Acrobat", "#B32020", "A"),
            ("FineReader", "#1B5E20", "F")]
    x0, y0 = px + 36, py + 106
    cw, ch = 100, 86
    for i, (name, col, letter) in enumerate(apps):
        cx = x0 + (i % 6) * (cw + 3)
        cy = y0 + (i // 6) * ch
        d.rounded_rectangle([cx + 8, cy + 4, cx + 60, cy + 56], radius=8, fill=col)
        d.text((cx + 34, cy + 30), letter, font=font(17, bold=True), fill="#FFFFFF",
               anchor="mm")
        label = name if len(name) <= 13 else name[:12] + "…"
        d.text((cx + 34, cy + 62), label, font=font(11), fill=TXT, anchor="ma")

    d.text((px + 34, py + 372), "Рекомендуем", font=font(15, bold=True), fill=TXT)
    recs = [("Документ Word", "Пароль для открытия.docx", "#2B579A", "W"),
            ("Отчёт.docx", "Практическая работа № 3", "#2B579A", "W"),
            ("Сведения о системе", "Утилита msinfo32", "#0F6CBD", "i"),
            ("Проводник", "Папка «Практическая работа № 3»", "#F2B90D", "П")]
    ry = py + 402
    for t, s, col, l in recs:
        d.rounded_rectangle([px + 30, ry, px + pw - 30, ry + 46], radius=6, fill="#FFFFFF")
        d.rounded_rectangle([px + 42, ry + 9, px + 70, ry + 37], radius=5, fill=col)
        d.text((px + 56, ry + 23), l, font=font(13, bold=True), fill="#FFFFFF", anchor="mm")
        d.text((px + 82, ry + 7), t, font=font(13), fill=TXT)
        d.text((px + 82, ry + 25), s, font=font(11), fill=MUTED)
        ry += 52

    # панель задач
    d.rectangle([0, H - 52, W, H], fill="#F2F2F2")
    d.ellipse([W // 2 - 44, H - 40, W // 2 - 20, H - 16], fill="#0F6CBD")
    d.rectangle([W // 2 - 38, H - 34, W // 2 - 34, H - 22], fill="#FFFFFF")
    d.rectangle([W // 2 - 34, H - 34, W // 2 - 26, H - 30], fill="#FFFFFF")
    d.rectangle([W // 2 - 34, H - 26, W // 2 - 26, H - 22], fill="#FFFFFF")
    d.text((W // 2 + 68, H - 40), "12:47", font=font(13), fill=TXT)
    d.text((W // 2 + 68, H - 26), "06.11.2026", font=font(11), fill=MUTED)
    img.save(os.path.join(OUT, "win_main_menu.png"), quality=95)
    print("IMG main menu")


def system_info():
    w = Win(1280, 820, "Сведения о системе", tabs=None, toolbar=["Файл", "Правка", "Вид", "Справка"],
            status="Сведения взяты с локального компьютера", margin=14)
    x0, y0, x1 = w.x0, w.cy0, w.x1
    # дерево
    tree_w = 330
    w.d.rectangle([x0 + 1, y0, x0 + tree_w, w.box[3] - 31], fill="#FFFFFF")
    w.d.line([x0 + tree_w, y0, x0 + tree_w, w.box[3] - 31], fill=LINE)
    w.text(x0 + 14, y0 + 10, "Система", 13, MUTED, bold=True)
    tree = [("Сведения о системе", 1, True), ("Ресурсы оборудования", 0, False),
            ("Конфликт/совместное использование", 1, False), ("DMA", 1, False),
            ("IRQ", 1, False), ("Ввод-вывод", 1, False), ("Память", 1, False),
            ("Компоненты", 0, False), ("Мультимедиа", 1, False), ("Звуковое устройство", 2, False),
            ("Дисплей", 1, False), ("Сеть", 1, False), ("Адаптер", 2, False),
            ("Печать", 1, False), ("Проблемные устройства", 1, False),
            ("Программная среда", 0, False), ("Переменные среды", 1, False),
            ("Системные драйверы", 1, False), ("Загруженные модули", 1, False),
            ("Службы", 1, False), ("Программы автозагрузки", 1, False)]
    ty = y0 + 34
    for name, lvl, sel in tree:
        if sel:
            w.d.rectangle([x0 + 1, ty - 2, x0 + tree_w, ty + 22], fill=SEL)
        if lvl > 0:
            al = x0 + 26 + lvl * 6
            w.d.line([x0 + 20, ty + 10, al - 4, ty + 10], fill="#B0B0B0")
            w.d.rectangle([al - 4, ty + 5, al + 6, ty + 15], outline="#8A8A8A")
            w.d.line([al - 1, ty + 10, al + 3, ty + 10], fill="#5A5A5A")
            if lvl == 1:
                w.d.line([al + 1, ty + 8, al + 1, ty + 12], fill="#5A5A5A")
            w.text(al + 8, ty, name, 13, TXT, bold=sel)
        else:
            w.d.rectangle([x0 + 14, ty + 5, x0 + 26, ty + 17], outline="#8A8A8A")
            w.d.text((x0 + 17, ty + 6), "-", font=font(11), fill=TXT)
            w.text(x0 + 32, ty, name, 13, TXT)
        ty += 26

    # таблица справа
    rx = x0 + tree_w + 1
    w.d.rectangle([rx, y0, x1 - 1, w.box[3] - 31], fill="#FFFFFF")
    hdr_y = y0 + 1
    w.d.rectangle([rx, hdr_y, x1 - 1, hdr_y + 26], fill="#F0F0F0")
    w.d.text((rx + 10, hdr_y + 5), "Элемент", font=font(13, bold=True), fill=TXT)
    w.d.text((rx + 520, hdr_y + 5), "Значение", font=font(13, bold=True), fill=TXT)
    w.d.line([rx, hdr_y + 26, x1 - 1, hdr_y + 26], fill="#C0C0C0")
    w.d.line([rx + 500, hdr_y, rx + 500, w.box[3] - 31], fill="#E0E0E0")
    rows = [
        ("Имя ОС", "Microsoft Windows 11 Pro"),
        ("Версия", "10.0.22631 сборка 22631"),
        ("Изготовитель ОС", "Microsoft Corporation"),
        ("Имя системы", "NGGTK-PC-47"),
        ("Изготовитель системы", "ASUS"),
        ("Модель системы", "ASUS ExpertCenter D500SC"),
        ("Тип системы", "x64-based PC"),
        ("Процессор", "Intel(R) Core(TM) i5-11400 @ 2.60GHz, 2601 МГц, 6 ядер, 12 логических"),
        ("Версия BIOS", "American Megatrends Inc. 3202, 15.03.2025"),
        ("Дата BIOS", "15.03.2025 00:00:00"),
        ("Объем установленной оперативной памяти", "16,0 ГБ"),
        ("Полный объем физической памяти", "15,8 ГБ"),
        ("Доступная физическая память", "9,24 ГБ"),
        ("Общий объем виртуальной памяти", "18,2 ГБ"),
        ("Файл подкачки", "C:\\pagefile.sys"),
        ("Домен", "WORKGROUP"),
        ("Рабочая группа", "WORKGROUP"),
        ("Тип ЦП", "Intel64 Family 6 Model 167 Stepping 1"),
        ("Имя компьютера", "NGGTK-PC-47"),
        ("Состояние безопасности загрузки", "Вкл."),
        ("Локаль", "Россия; Русский (Россия)"),
        ("Часовой пояс", "UTC+04:00 Самара"),
        ("Сеть", "Realtek PCIe GbE Family Controller, IP 192.168.1.24"),
        ("Обновление Windows", "Обновления установлены 02.11.2026"),
    ]
    ry = hdr_y + 28
    for i, (k, v) in enumerate(rows):
        if i % 2 == 1:
            w.d.rectangle([rx + 1, ry - 3, x1 - 2, ry + 21], fill="#FAFAFA")
        w.text(rx + 10, ry, k, 12, TXT)
        w.fit(rx + 516, ry, v, x1 - rx - 530, 12, TXT)
        ry += 24
    w.save(os.path.join(OUT, "win_systeminfo.png"))


if __name__ == "__main__":
    start_menu()
    system_info()


def spo_scheme():
    from flow import Flow, BLUE, LBLUE, GREEN, GREENL, ORANGE, ORANGEL, GREY
    f = Flow(1400, 760, margin=10)
    f.title("Структура программного обеспечения ПЭВМ")
    f.block("po", 560, 76, 280, 56, "Программное обеспечение (ПО)", "rect", "#DCE9F7", BLUE, 16)
    b1 = f.block("sys", 60, 216, 250, 106, "Системное ПО\n(СПО)", "rect", LBLUE, BLUE, 16)
    b2 = f.block("app", 585, 216, 250, 106, "Прикладное ПО\n(ППО)", "rect", GREEN, GREENL, 16)
    b3 = f.block("ins", 1120, 216, 250, 106, "Инструментальное\n(системы программирования)",
                 "rect", ORANGE, ORANGEL, 15)
    f.link("po", "sys")
    f.link("po", "app")
    f.link("po", "ins")

    items = [
        (["Операционные системы", "Драйверы", "Сервисные системы\n(утилиты, архиваторы,\nантивирусы)"], 60),
        (["Текстовые редакторы,\nофисные пакеты", "СУБД", "Графические редакторы",
          "Обучающие программы,\nигры"], 585),
        (["Трансляторы\n(компиляторы,\nинтерпретаторы)", "Среды разработки", "Отладчики",
          "Исходные тексты\nи документация"], 1120),
    ]
    for lst, x in items:
        y = 372
        for t in lst:
            h = 78 if "\n" in t else 50
            f.block(f"i_{x}_{y}_{t[:6]}", x + 8, y, 234, h, t, "rect", "#FFFFFF",
                    "#9AA9B8", 14, bold=False)
            f.link("sys" if x == 60 else ("app" if x == 585 else "ins"),
                   f"i_{x}_{y}_{t[:6]}", dashed=True, head=False, width=1,
                   color="#9AA9B8")
            y += h + 22
    f.caption(30, f.H - 34, "Классификация ПО по функциональному признаку", 13, "#5D5D5D")
    f.save(os.path.join(OUT, "scheme_spo.png"))


if __name__ == "__main__":
    spo_scheme()
