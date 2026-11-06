# -*- coding: utf-8 -*-
"""Иллюстрации к ПЗ № 4 (МДК 06.02): редактор реестра, архивация состояния системы."""
import os

from PIL import Image, ImageDraw

from mockui import (ACCENT, LINE, MUTED, SEL, TXT, WHITE, Win, dialog, dialog_buttons,
                    font, str_list, text_field, win_modal, text_field)

OUT = "/home/user/-/Выполненные работы/Иллюстрации/ПЗ_4_МДК_06.02_реестр_и_архивация"
os.makedirs(OUT, exist_ok=True)


TREE = [("HKEY_CLASSES_ROOT", 0), ("HKEY_CURRENT_USER", 0), ("HKEY_LOCAL_MACHINE", 0),
        ("BCD00000000", 1), ("HARDWARE", 1), ("SAM", 1), ("SECURITY", 1),
        ("SOFTWARE", 1), ("SYSTEM", 1), ("HKEY_USERS", 0), ("HKEY_CURRENT_CONFIG", 0)]


def regedit_base(selected="SOFTWARE", values=None, status="Готово"):
    w = Win(1250, 800, "Редактор реестра", margin=12,
            toolbar=["Файл", "Правка", "Вид", "Избранное", "Справка"])
    x0, y0, x1 = w.x0, w.cy0, w.x1
    tw = 420
    w.d.rectangle([x0 + 1, y0, x0 + tw, w.box[3] - 31], fill=WHITE)
    w.d.line([x0 + tw, y0, x0 + tw, w.box[3] - 31], fill=LINE)
    w.text(x0 + 14, y0 + 8, "Компьютер", 13, TXT, bold=True)
    ty = y0 + 34
    for name, lvl in TREE:
        if lvl == 0:
            w.d.rectangle([x0 + 14, ty + 5, x0 + 26, ty + 17], outline="#8A8A8A")
            w.d.text((x0 + 17, ty + 6), "-", font=font(11), fill=TXT)
            sel = (name == "HKEY_LOCAL_MACHINE")
            w.text(x0 + 32, ty, name, 13, TXT, bold=sel)
            if sel:
                w.d.rectangle([x0 + 1, ty - 3, x0 + tw, ty + 21], fill=SEL)
                w.text(x0 + 32, ty, name, 13, TXT, bold=True)
            ty += 26
        else:
            indent = x0 + 62
            sub_sel = (name == selected)
            w.d.line([x0 + 46, ty + 10, indent - 6, ty + 10], fill="#B0B0B0")
            w.d.rectangle([indent - 6, ty + 5, indent + 4, ty + 15], outline="#8A8A8A")
            w.d.line([indent - 3, ty + 10, indent + 1, ty + 10], fill="#5A5A5A")
            if sub_sel and name != "SYSTEM":
                w.d.rectangle([x0 + 1, ty - 3, x0 + tw, ty + 21], fill=SEL)
            w.text(indent + 8, ty, name, 13, TXT, bold=sub_sel)
            ty += 26
    # правая часть — значения
    w.d.rectangle([x0 + tw + 1, y0, x1 - 1, w.box[3] - 31], fill=WHITE)
    hdr = y0 + 1
    w.d.rectangle([x0 + tw + 1, hdr, x1 - 1, hdr + 26], fill="#F0F0F0")
    w.text(x0 + tw + 12, hdr + 5, "Имя", 13, TXT, bold=True)
    w.text(x0 + tw + 250, hdr + 5, "Тип", 13, TXT, bold=True)
    w.text(x0 + tw + 430, hdr + 5, "Значение", 13, TXT, bold=True)
    w.d.line([x0 + tw + 1, hdr + 26, x1 - 1, hdr + 26], fill="#C0C0C0")
    vals = values or [
        ("(По умолчанию)", "REG_SZ", "(значение не присвоено)"),
        ("CurrentBuild", "REG_SZ", "22631"),
        ("CurrentVersion", "REG_SZ", "6.3"),
        ("ProductName", "REG_SZ", "Windows 11 Pro"),
        ("RegisteredOwner", "REG_SZ", "Разин К.Е."),
        ("RegisteredOrganization", "REG_SZ", "НГГТК"),
        ("InstallDate", "REG_DWORD", "0x61F2A4C1 (1649сут)"),
        ("InstallTime", "REG_QWORD", "0x01d9c4f2a8b13e77"),
        ("SystemRoot", "REG_SZ", "C:\\Windows"),
    ]
    ry = hdr + 30
    for i, (n, t, v) in enumerate(vals):
        if i == 4:
            w.d.rectangle([x0 + tw + 1, ry - 3, x1 - 1, ry + 21], fill=SEL)
        w.fit(x0 + tw + 12, ry, n, 225, 12, TXT)
        w.text(x0 + tw + 250, ry, t, 12, MUTED)
        w.fit(x0 + tw + 430, ry, v, x1 - (x0 + tw + 440), 12, TXT)
        ry += 24
    w.statusbar(status)
    return w


def regedit_export_menu():
    w = regedit_base(status="Мой компьютер\\HKEY_LOCAL_MACHINE\\SOFTWARE")
    x0, y0 = w.x0, w.cy0
    items = [("Импорт…", "Ctrl+I"), ("Экспорт…", "Ctrl+E"), (None, None),
             ("Загрузить куст…", ""), ("Выгрузить куст…", ""), (None, None),
             ("Подключить сетевой диск…", ""), ("Отключить сетевой диск…", ""),
             (None, None), ("Печать…", "Ctrl+P"), ("Выход", "")]
    h = 32
    total = sum(h if it[0] else 9 for it in items) + 12
    box = (x0 + 14, y0 + 2, x0 + 250, y0 + 2 + total)
    w.d.rounded_rectangle([box[0] + 3, box[1] + 4, box[2] + 3, box[3] + 4], radius=4,
                          fill="#DDDDDD")
    w.d.rounded_rectangle(box, radius=4, fill="#FBFBFB", outline="#C4C4C4")
    cy = box[1] + 6
    for i, (it, key) in enumerate(items):
        if it is None:
            w.d.line([box[0] + 10, cy + 4, box[2] - 10, cy + 4], fill=LINE)
            cy += 9
            continue
        if i == 1:
            w.d.rounded_rectangle([box[0] + 4, cy, box[2] - 4, cy + h - 4], radius=3,
                                  fill=SEL)
        w.text(box[0] + 16, cy + 6, it, 13, TXT)
        if key:
            w.text(box[2] - 14, cy + 8, key, 11, MUTED, anchor="ra")
        cy += h
    w.statusbar("Мой компьютер\\HKEY_LOCAL_MACHINE\\SOFTWARE   |   Выбрано: SOFTWARE")
    w.save(os.path.join(OUT, "regedit_export_menu.png"))


def regedit_export_dialog():
    img, d, box = dialog("Экспорт файла реестра", 720, 430, 1250, 800)
    x, y = box[0], box[1]
    d.text((x + 26, y + 58), "Папка:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 26, y + 80, x + 560, y + 108], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 36, y + 86), "D:\\Практическая работа № 4", font=font(13), fill=TXT)
    d.text((x + 470, y + 85), "▾", font=font(11), fill=MUTED)
    d.rounded_rectangle([x + 580, y + 80, x + 694, y + 108], radius=3, fill="#F3F3F3",
                        outline="#B0B0B0")
    d.text((x + 610, y + 86), "Обзор…", font=font(12), fill=TXT)
    # список файлов
    d.rectangle([x + 26, y + 118, x + 560, y + 230], fill=WHITE, outline="#C0C0C0")
    d.rectangle([x + 27, y + 119, x + 559, y + 143], fill="#F0F0F0")
    d.text((x + 36, y + 123), "Имя", font=font(12, bold=True), fill=TXT)
    d.text((x + 330, y + 123), "Дата изменения", font=font(12, bold=True), fill=TXT)
    files = [("Отчет.docx", "06.11.2026 12:44"),
             ("Разин_КЭ_реестр.reg", "06.11.2026 12:52"),
             ("Снимок_реестра_полный.reg", "06.11.2026 12:55")]
    ry = y + 148
    for i, (n, dt) in enumerate(files):
        if i == 1:
            d.rectangle([x + 27, ry - 3, x + 559, ry + 20], fill=SEL)
        d.text((x + 36, ry), n, font=font(12), fill=TXT)
        d.text((x + 330, ry), dt, font=font(11), fill=MUTED)
        ry += 24
    d.text((x + 26, y + 244), "Имя файла:", font=font(13), fill=TXT)
    text_field(d, x + 26, y + 266, 430, "Разин_КЭ_реестр.reg", 30, 13, focused=True)
    d.text((x + 470, y + 272), "Тип файлов: Файлы реестра (*.reg)", font=font(11), fill=MUTED)
    d.text((x + 26, y + 312), "Диапазон экспорта", font=font(13, bold=True), fill=TXT)
    d.ellipse([x + 26, y + 338, x + 40, y + 352], outline="#8A8A8A", fill=WHITE)
    d.ellipse([x + 30, y + 342, x + 36, y + 348], fill=ACCENT)
    d.text((x + 50, y + 334), "Вся ветвь", font=font(13), fill=TXT)
    d.ellipse([x + 200, y + 338, x + 214, y + 352], outline="#8A8A8A", fill=WHITE)
    d.text((x + 224, y + 334), "Выбранная ветвь", font=font(13), fill=MUTED)
    dialog_buttons(d, box, ("Сохранить", "Отмена"), y=y + 368)
    img.save(os.path.join(OUT, "regedit_export_dialog.png"))
    print("IMG export dialog")


def regedit_import_dialog():
    img, d, box = dialog("Импорт файла реестра", 720, 400, 1250, 800)
    x, y = box[0], box[1]
    d.text((x + 26, y + 58), "Папка:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 26, y + 80, x + 560, y + 108], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 36, y + 86), "D:\\Практическая работа № 4", font=font(13), fill=TXT)
    d.text((x + 470, y + 85), "▾", font=font(11), fill=MUTED)
    d.rectangle([x + 26, y + 118, x + 560, y + 240], fill=WHITE, outline="#C0C0C0")
    d.rectangle([x + 27, y + 119, x + 559, y + 143], fill="#F0F0F0")
    d.text((x + 36, y + 123), "Имя", font=font(12, bold=True), fill=TXT)
    d.text((x + 330, y + 123), "Дата изменения", font=font(12, bold=True), fill=TXT)
    files = [("Разин_КЭ_реестр.reg", "06.11.2026 12:52"),
             ("Снимок_реестра_полный.reg", "06.11.2026 12:55")]
    ry = y + 148
    for i, (n, dt) in enumerate(files):
        if i == 0:
            d.rectangle([x + 27, ry - 3, x + 559, ry + 20], fill=SEL)
        d.text((x + 36, ry), n, font=font(12), fill=TXT)
        d.text((x + 330, ry), dt, font=font(11), fill=MUTED)
        ry += 24
    d.text((x + 26, y + 252), "Имя файла:", font=font(13), fill=TXT)
    text_field(d, x + 26, y + 274, 430, "Разин_КЭ_реестр.reg", 30, 13, focused=True)
    d.text((x + 26, y + 314), "Файлы реестра (*.reg)", font=font(11), fill=MUTED)
    dialog_buttons(d, box, ("Открыть", "Отмена"), y=y + 340)
    img.save(os.path.join(OUT, "regedit_import_dialog.png"))
    print("IMG import dialog")


def regedit_confirm():
    img, d, box = dialog("Предупреждение редактора реестра", 640, 300, 1250, 800)
    x, y = box[0], box[1]
    d.ellipse([x + 30, y + 66, x + 76, y + 112], fill="#FDF3D6")
    d.text((x + 53, y + 78), "!", font=font(24, bold=True), fill="#B8860B", anchor="ma")
    d.text((x + 96, y + 66), "Добавление сведений в реестр может", font=font(14), fill=TXT)
    d.text((x + 96, y + 90), "привести к непредсказуемым последствиям.", font=font(14), fill=TXT)
    d.text((x + 96, y + 118), "Файл: Разин_КЭ_реестр.reg", font=font(12), fill=MUTED)
    d.rectangle([x + 96, y + 151, x + 112, y + 167], outline="#8A8A8A", fill=WHITE)
    d.text((x + 120, y + 148), "Больше не показывать это предупреждение", font=font(13),
           fill=TXT)
    d.text((x + 30, y + 190), "Продолжить импорт выбранного файла?", font=font(14, bold=True),
           fill=TXT)
    dialog_buttons(d, box, ("Да", "Нет"), y=y + 232)
    img.save(os.path.join(OUT, "regedit_confirm.png"))
    print("IMG confirm")


def backup_tool():
    w = Win(1250, 800, "Архивация и восстановление файлов — Мастер архивации", margin=12,
            status="Идёт архивация: D:\\Практическая работа № 4\\Резервная_копия.bkf")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F7F9FC")
    w.sidebar(x0 + 1, y0, 260, ["Архивация", "Восстановление", "Планирование",
                                "Журнал", "Параметры"], active=0, title="МАСТЕР")
    w.text(x0 + 290, y0 + 18, "Архивация файлов и параметров", 17, TXT, bold=True)
    w.text(x0 + 290, y0 + 50, "Выберите объекты, которые нужно включить в архив",
           13, MUTED)
    # дерево объектов
    w.panel(x0 + 290, y0 + 78, 900, 336)
    w.d.rectangle([x0 + 300, y0 + 88, x1 - 30, y0 + 114], fill="#EDF1F6")
    w.text(x0 + 312, y0 + 93, "Объекты архивации", 13, TXT, bold=True)
    w.text(x0 + 760, y0 + 93, "Размер", 13, TXT, bold=True)
    tree = [("Мой компьютер", 0, False, True),
            ("Состояние системы", 1, True, False),
            ("Документы и параметры (C:\\Users\\Student)", 1, False, True),
            ("Рабочий стол пользователя", 2, True, False),
            ("Мои документы", 2, True, False),
            ("Локальный диск (D:)", 1, False, False),
            ("Практическая работа № 4", 2, True, False),
            ("Практическая работа № 3", 2, True, False),
            ("Съёмный диск (E:)", 1, False, False)]
    ry = y0 + 120
    for name, lvl, chk, plus in tree:
        tx = x0 + 312 + lvl * 22
        if chk:
            d_x = tx
            w.d.rectangle([d_x, ry + 4, d_x + 14, ry + 18], fill=ACCENT, outline="#7A7A7A")
            w.d.line([d_x + 3, ry + 11, d_x + 6, ry + 14], fill=WHITE, width=2)
            w.d.line([d_x + 6, ry + 14, d_x + 11, ry + 7], fill=WHITE, width=2)
        else:
            w.d.rectangle([tx, ry + 4, tx + 14, ry + 18], outline="#8A8A8A", fill=WHITE)
        ix = tx + 22
        if lvl == 0 or plus:
            w.d.rectangle([ix, ry + 5, ix + 11, ry + 16], outline="#8A8A8A")
            w.d.text((ix + 2, ry + 5), "-" if lvl == 0 else "+", font=font(10), fill=TXT)
        ix += 18
        w.d.rounded_rectangle([ix, ry + 4, ix + 16, ry + 18], radius=2,
                              fill="#F2B90D" if "диск" in name.lower() or "Диск" in name
                              else "#2B579A")
        w.text(ix + 24, ry, name, 13, TXT, bold=(lvl <= 1))
        if lvl == 1 and "Состояние" in name:
            w.text(x0 + 760, ry, "2,4 ГБ", 13, TXT)
        ry += 30
    # прогресс
    w.panel(x0 + 290, y0 + 428, 900, 196)
    w.text(x0 + 312, y0 + 442, "Ход выполнения архивации", 14, TXT, bold=True)
    w.d.rounded_rectangle([x0 + 312, y0 + 472, x1 - 52, y0 + 496], radius=8, fill="#E3E7ED")
    w.d.rounded_rectangle([x0 + 312, y0 + 472, x0 + 312 + 610, y0 + 496], radius=8,
                          fill=ACCENT)
    w.fit(x0 + 312, y0 + 506, "68 %  —  архивируется C:\\Windows\\System32\\config\\SYSTEM", 640, 12, MUTED)
    w.text(x0 + 312, y0 + 532, "Обработано файлов: 18 427 из 27 100", 12, MUTED)
    w.text(x0 + 312, y0 + 558, "Место назначения: D:\\Практическая работа № 4\\"
           "Резервная_копия.bkf", 12, MUTED)
    w.text(x1 - 250, y0 + 506, "Тип архива: Обычный", 12, MUTED)
    w.text(x1 - 250, y0 + 532, "Начало: 12:58:14", 12, MUTED)
    w.button(x0 + 290, w.box[3] - 74, 150, "Архивировать", primary=True, h=32)
    w.button(x0 + 452, w.box[3] - 74, 120, "Отмена", h=32)
    w.button(x0 + 584, w.box[3] - 74, 150, "Дополнительно…", h=32)
    w.statusbar("Идёт архивация: D:\\Практическая работа № 4\\Резервная_копия.bkf")
    w.save(os.path.join(OUT, "backup_tool.png"))


def backup_restore():
    w = Win(1250, 800, "Архивация и восстановление файлов — Восстановление", margin=12,
            status="Готово к восстановлению")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F7F9FC")
    w.sidebar(x0 + 1, y0, 260, ["Архивация", "Восстановление", "Планирование",
                                "Журнал", "Параметры"], active=1, title="МАСТЕР")
    w.text(x0 + 290, y0 + 18, "Восстановление файлов и параметров", 17, TXT, bold=True)
    w.text(x0 + 290, y0 + 50, "Укажите архив и объекты для восстановления", 13, MUTED)
    w.panel(x0 + 290, y0 + 78, 900, 300)
    w.text(x0 + 312, y0 + 92, "Каталог носителя", 13, TXT, bold=True)
    w.d.rounded_rectangle([x0 + 312, y0 + 116, x0 + 690, y0 + 144], radius=3, fill=WHITE,
                          outline="#B0B0B0")
    w.text(x0 + 322, y0 + 122, "D:\\Практическая работа № 4\\Резервная_копия.bkf",
           12, TXT)
    w.button(x0 + 700, y0 + 116, 110, "Обзор…", h=28, size=12)
    w.d.rectangle([x0 + 312, y0 + 158, x1 - 52, y0 + 184], fill="#EDF1F6")
    for lab, cx in [("Файл/папка", x0 + 322), ("Размер", x0 + 620), ("Дата", x0 + 760)]:
        w.text(cx, y0 + 163, lab, 12, TXT, bold=True)
    rows = [("Состояние системы", "2,4 ГБ", "06.11.2026 12:58"),
            ("C:\\Users\\Student\\Документы", "612 МБ", "06.11.2026 12:58"),
            ("D:\\Практическая работа № 4", "48 МБ", "06.11.2026 12:58"),
            ("D:\\Практическая работа № 3", "36 МБ", "06.11.2026 12:58")]
    ry = y0 + 190
    for i, (n, sz, dt) in enumerate(rows):
        if i == 0:
            w.d.rectangle([x0 + 311, ry - 3, x1 - 51, ry + 21], fill=SEL)
        w.d.rectangle([x0 + 322, ry + 3, x0 + 336, ry + 17], fill=ACCENT)
        w.d.line([x0 + 325, ry + 10, x0 + 328, ry + 13], fill=WHITE, width=2)
        w.d.line([x0 + 328, ry + 13, x0 + 333, ry + 6], fill=WHITE, width=2)
        w.text(x0 + 346, ry, n, 13, TXT, bold=(i == 0))
        w.text(x0 + 620, ry, sz, 13, TXT)
        w.text(x0 + 760, ry, dt, 13, MUTED)
        ry += 30
    w.panel(x0 + 290, y0 + 396, 900, 240)
    w.text(x0 + 312, y0 + 410, "Параметры восстановления", 14, TXT, bold=True)
    w.radio(x0 + 312, y0 + 442, "Восстановить в исходное расположение", True, 13)
    w.radio(x0 + 312, y0 + 474, "Восстановить в альтернативное расположение",
            False, 13)
    w.d.rounded_rectangle([x0 + 340, y0 + 500, x0 + 690, y0 + 528], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x0 + 350, y0 + 506, "D:\\Восстановление", 12, MUTED)
    w.checkbox(x0 + 312, y0 + 546, "Заменить существующие файлы", True, 13)
    w.checkbox(x0 + 312, y0 + 578, "Восстановить права доступа и параметры "
               "безопасности", True, 13)
    w.button(x0 + 290, y0 + 656, 160, "Восстановить", primary=True, h=32)
    w.button(x0 + 462, y0 + 656, 120, "Отмена", h=32)
    w.statusbar("Готово к восстановлению")
    w.save(os.path.join(OUT, "backup_restore.png"))


def command_run():
    img, d, box = dialog("Выполнить", 620, 220, 1250, 800)
    x, y = box[0], box[1]
    d.text((x + 26, y + 58), "Введите имя программы, папки или документа:", font=font(13), fill=TXT)
    text_field(d, x + 26, y + 86, 560, "regedit", 32, 14, focused=True)
    d.text((x + 26, y + 130), "Открыть:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 110, y + 124, x + 586, y + 154], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 120, y + 131), "C:\\Windows\\System32\\regedit.exe", font=font(12), fill=TXT)
    d.text((x + 560, y + 130), "▾", font=font(11), fill=MUTED)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=y + 176)
    img.save(os.path.join(OUT, "run_dialog.png"))
    print("IMG run dialog")


def regedit_values_export_done():
    w = regedit_base(status="Экспорт диапазона «Мой компьютер\\HKEY_LOCAL_MACHINE\\SOFTWARE» "
                     "выполнен. Файл сохранён")
    x0, y0 = w.x0, w.cy0
    d, box = win_modal(w, 620, 260, "Экспорт реестра", y_off=20)
    bx, by = box[0], box[1]
    d.ellipse([bx + 28, by + 66, bx + 74, by + 112], fill="#E3F3E4")
    d.line([bx + 40, by + 88, bx + 48, by + 98], fill="#2E7D32", width=4)
    d.line([bx + 48, by + 98, bx + 62, by + 78], fill="#2E7D32", width=4)
    d.text((bx + 94, by + 62), "Файл успешно экспортирован", font=font(15, bold=True), fill=TXT)
    d.text((bx + 94, by + 94), "Разин_КЭ_реестр.reg", font=font(13), fill=TXT)
    d.text((bx + 94, by + 118), "Размер: 1,84 МБ   |   Объектов: 214 573", font=font(12),
           fill=MUTED)
    d.text((bx + 94, by + 142), "D:\\Практическая работа № 4", font=font(12), fill=MUTED)
    dialog_buttons(d, box, ("ОК",), y=by + 196)
    d.rounded_rectangle([bx + 480, by + 196, bx + 580, by + 228], radius=4, fill=ACCENT)
    d.text((bx + 530, by + 204), "ОК", font=font(14), fill=WHITE, anchor="ma")
    w.statusbar("Экспорт ветви HKEY_LOCAL_MACHINE\\SOFTWARE выполнен успешно")
    w.save(os.path.join(OUT, "regedit_export_done.png"))


if __name__ == "__main__":
    regedit_export_menu()
    regedit_export_dialog()
    regedit_import_dialog()
    regedit_confirm()
    backup_tool()
    backup_restore()
    command_run()
    regedit_values_export_done()
