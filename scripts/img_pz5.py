# -*- coding: utf-8 -*-
"""Иллюстрации к ПЗ № 5 (МДК 06.02): SQL Server Management Studio, резервное копирование БД."""
import os

from PIL import Image, ImageDraw

from mockui import (ACCENT, LINE, MUTED, SEL, TXT, WHITE, Win, dialog, dialog_buttons,
                    font, mbutton, text_field, win_modal)

OUT = "/tmp/img/pz5"
os.makedirs(OUT, exist_ok=True)
SSMS = "#0F6CBD"


def ssms(title, tabs=("LibraryDB.sql*", "Запрос1.sql"), status="Готово",
         tree_sel=("LibraryDB", "Базы данных"), show_query=False, results=None):
    w = Win(1280, 820, title, margin=12, accent=SSMS,
            toolbar=["Файл", "Правка", "Вид", "Сервис", "Окно", "Справка"])
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F5F6F8")
    # панель вкладок документов
    w.d.rectangle([x0 + 1, y0, x1 - 1, y0 + 28], fill="#ECEEF1")
    tx = x0 + 8
    for i, t in enumerate(tabs):
        tw = int(w.d.textlength(t, font=font(12))) + 30
        if i == 0:
            w.d.rectangle([tx, y0 + 2, tx + tw, y0 + 28], fill=WHITE)
            w.d.line([tx, y0 + 2, tx + tw, y0 + 2], fill=SSMS, width=2)
            w.text(tx + 12, y0 + 7, t, 12, TXT)
        else:
            w.text(tx + 12, y0 + 7, t, 12, MUTED)
        tx += tw + 4
    ey = y0 + 28
    # Object Explorer
    ow = 350
    w.d.rectangle([x0 + 1, ey, x0 + ow, ey + 26], fill="#DDE3EA")
    w.text(x0 + 12, ey + 5, "Обозреватель объектов", 12, TXT, bold=True)
    w.d.rectangle([x0 + 1, ey + 26, x0 + ow, w.box[3] - 31], fill="#FBFCFD")
    w.d.line([x0 + ow, ey, x0 + ow, w.box[3] - 31], fill="#C9CFD6")
    nodes = [("NGGTK-SQL\\SQLEXPRESS (SQL Server 15.0.4322)", 0, False),
             ("Базы данных", 1, True), ("Системные базы данных", 2, False),
             ("LibraryDB", 2, True), ("Диаграммы базы данных", 3, False),
             ("Таблицы", 3, False), ("Представления", 3, False),
             ("Программируемость", 3, False), ("Безопасность", 2, False),
             ("Отчеты", 1, False), ("Безопасность", 1, False),
             ("Объекты сервера", 1, False), ("Репликация", 1, False),
             ("Управление", 1, False)]
    ty = ey + 36
    for name, lvl, act in nodes:
        ix = x0 + 12 + lvl * 16
        if lvl < 3:
            w.d.rectangle([ix, ty + 5, ix + 10, ty + 15], outline="#8A8A8A")
            w.d.text((ix + 2, ty + 5), "-" if lvl < 2 else "+", font=font(9), fill=TXT)
            ix += 14
        else:
            ix += 24
        if act and name == "LibraryDB":
            w.d.rectangle([x0 + 2, ty - 3, x0 + ow, ty + 19], fill="#D6E4F5")
        w.d.rounded_rectangle([ix, ty + 3, ix + 12, ty + 15], radius=2,
                              fill="#D9A441" if lvl == 1 else
                              ("#4C8FBF" if lvl == 2 else "#8FA8BE"))
        w.text(ix + 18, ty, name, 12, TXT, bold=(name == "LibraryDB"))
        ty += 23
    # рабочая область
    cx = x0 + ow + 1
    if show_query:
        w.d.rectangle([cx, ey, x1 - 1, w.box[3] - 31], fill=WHITE)
        w.d.rectangle([cx, ey, x1 - 1, ey + 28], fill="#F3F3F3")
        w.button(cx + 12, ey + 4, 90, "Выполнить", primary=True, h=22, size=12)
        w.text(cx + 116, ey + 8, "LibraryDB (SQL Server 15.0)", 12, MUTED)
        w.text(x1 - 130, ey + 8, "master", 12, MUTED)
        w.d.line([cx, ey + 28, x1 - 1, ey + 28], fill="#D0D0D0")
        qy = ey + 42
        if results:
            sql_lines, res = results
            ln = 1
            for s in sql_lines:
                w.text(cx + 10, qy - 1, f"{ln}", 12, "#9A9A9A", mono=True)
                parts = s.split("--")
                w.text(cx + 42, qy, s, 13, "#1B3A5B", mono=True)
                qy += 21
                ln += 1
            qy += 14
            w.d.line([cx, qy - 6, x1 - 1, qy - 6], fill="#D0D0D0")
            w.d.rectangle([cx, qy, x1 - 1, qy + 24], fill="#E8EAED")
            w.text(cx + 12, qy + 5, "Результаты", 12, TXT, bold=True)
            w.text(cx + 110, qy + 5, "Сообщения", 12, MUTED)
            gy = qy + 28
            w.d.rectangle([cx + 8, gy, cx + 8 + 620, gy + 24], fill="#EDF1F6")
            w.text(cx + 16, gy + 5, res[0][0], 12, TXT, bold=True)
            ry = gy + 28
            for row in res[1:]:
                w.d.rectangle([cx + 8, ry, cx + 8 + 620, ry + 22], fill=WHITE,
                              outline="#E3E3E3")
                w.text(cx + 16, ry + 4, row, 12, TXT, mono=True)
                ry += 22
            w.text(cx + 12, ry + 8, "Базе данных «LibraryDB» создана резервная копия.", 12, MUTED)
    else:
        w.d.rectangle([cx, ey, x1 - 1, w.box[3] - 31], fill="#F0F2F5")
        w.text((cx + x1) / 2, (ey + w.box[3]) / 2 - 20,
               "Чтобы начать работу, подключитесь к базе данных", 14, MUTED, anchor="ma")
        w.text((cx + x1) / 2, (ey + w.box[3]) / 2 + 8,
               "NGGTK-SQL\\SQLEXPRESS  •  LibraryDB", 12, MUTED, anchor="ma")
    w.statusbar(status, "Строка 1   Столбец 1")
    return w, ey


def connect_dialog():
    img, d, box = dialog("Соединение с сервером", 660, 470, 1280, 820)
    x, y = box[0], box[1]
    d.text((x + 26, y + 56), "Тип сервера:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 170, y + 50, x + 610, y + 78], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 180, y + 56), "Ядро СУБД", font=font(13), fill=TXT)
    d.text((x + 590, y + 55), "▾", font=font(11), fill=MUTED)
    d.text((x + 26, y + 96), "Имя сервера:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 170, y + 90, x + 610, y + 118], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 180, y + 96), "NGGTK-SQL\\SQLEXPRESS", font=font(13), fill=TXT)
    d.text((x + 590, y + 95), "▾", font=font(11), fill=MUTED)
    d.text((x + 26, y + 136), "Проверка подлинности:", font=font(13), fill=TXT)
    d.rounded_rectangle([x + 170, y + 130, x + 610, y + 158], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 180, y + 136), "Проверка подлинности SQL Server", font=font(13), fill=TXT)
    d.text((x + 590, y + 135), "▾", font=font(11), fill=MUTED)
    d.text((x + 26, y + 176), "Имя входа:", font=font(13), fill=TXT)
    text_field(d, x + 170, y + 170, 300, "sa", 30, 13)
    d.text((x + 26, y + 216), "Пароль:", font=font(13), fill=TXT)
    text_field(d, x + 170, y + 210, 300, "••••••••••", 30, 13)
    d.rectangle([x + 170, y + 252, x + 186, y + 268], fill=ACCENT, outline="#8A8A8A")
    d.line([x + 174, y + 260, x + 177, y + 264], fill=WHITE, width=2)
    d.line([x + 177, y + 264, x + 183, y + 256], fill=WHITE, width=2)
    d.text((x + 194, y + 250), "Запомнить пароль", font=font(13), fill=TXT)
    d.text((x + 26, y + 296), "Имя базы данных:", font=font(13), fill=MUTED)
    d.rounded_rectangle([x + 170, y + 290, x + 610, y + 318], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((x + 180, y + 296), "LibraryDB", font=font(13), fill=TXT)
    d.text((x + 26, y + 352), "Состояние подключения:", font=font(13), fill=TXT)
    d.text((x + 200, y + 352), "Подключено успешно", font=font(13), fill="#2E7D32", bold=True)
    d.line([x + 24, y + 384, x + 636, y + 384], fill="#DDDDDD")
    dialog_buttons(d, box, ("Подключить", "Отмена", "Справка"), y=y + 400)
    img.save(os.path.join(OUT, "ssms_connect.png"))
    print("IMG ssms_connect")


def recovery_simple():
    w, ey = ssms("NGGTK-SQL\\SQLEXPRESS (SQL Server 15.0.4322) — Microsoft SQL Server "
                 "Management Studio", show_query=True, results=(
        ["USE master;",
         "GO",
         "ALTER DATABASE LibraryDB",
         "SET RECOVERY SIMPLE;",
         "GO",
         "SELECT DATABASEPROPERTYEX('LibraryDB','Recovery') AS RecoveryModel;"],
        [("RecoveryModel"), ("SIMPLE")]))
    w.statusbar("Запрос выполнен успешно   |   Время выполнения: 00:00:00,014   |   1 строка",
                "NGGTK-SQL (15.0 RTM)")
    w.save(os.path.join(OUT, "ssms_recovery_simple.png"))


def backup_general():
    w, ey = ssms("Microsoft SQL Server Management Studio — LibraryDB", show_query=False)
    x0 = w.x0
    d, box = win_modal(w, 900, 600, "Резервное копирование базы данных — LibraryDB",
                       y_off=-10)
    bx, by = box[0], box[1]
    # вкладки
    tabs = ["Общие", "Параметры носителя", "Параметры резервного копирования",
            "Дополнительно"]
    tx = bx + 24
    for i, t in enumerate(tabs):
        tw = int(d.textlength(t, font=font(13))) + 24
        if i == 0:
            d.rectangle([tx, by + 46, tx + tw, by + 78], fill=WHITE)
            d.line([tx, by + 46, tx + tw, by + 46], fill=SSMS, width=2)
            d.text((tx + 12, by + 54), t, font=font(13, bold=True), fill=TXT)
        else:
            d.text((tx + 12, by + 54), t, font=font(13), fill=MUTED)
        tx += tw + 2
    d.line([bx + 24, by + 79, bx + 876, by + 79], fill="#C8C8C8")
    d.text((bx + 26, by + 96), "Источник", font=font(14, bold=True), fill=TXT)
    d.text((bx + 26, by + 130), "База данных:", font=font(13), fill=TXT)
    d.rounded_rectangle([bx + 210, by + 124, bx + 570, by + 152], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((bx + 220, by + 130), "LibraryDB", font=font(13), fill=TXT)
    d.text((bx + 552, by + 129), "▾", font=font(11), fill=MUTED)
    d.text((bx + 26, by + 164), "Модель восстановления:", font=font(13), fill=TXT)
    d.text((bx + 210, by + 164), "SIMPLE", font=font(13), bold=True, fill=TXT)
    d.text((bx + 26, by + 194), "Тип резервной копии:", font=font(13), fill=TXT)
    d.rounded_rectangle([bx + 210, by + 188, bx + 570, by + 216], radius=3, fill=WHITE,
                        outline="#B0B0B0")
    d.text((bx + 220, by + 194), "Полная", font=font(13), fill=TXT)
    d.text((bx + 552, by + 193), "▾", font=font(11), fill=MUTED)
    d.text((bx + 26, by + 226), "Компонент:", font=font(13), fill=TXT)
    d.text((bx + 210, by + 226), "Базы данных", font=font(13), fill=TXT)
    d.text((bx + 26, by + 252), "Имя резервного набора:", font=font(13), fill=TXT)
    text_field(d, bx + 210, by + 246, 360, "LibraryDB-Full Database Backup", 28, 12)
    d.line([bx + 24, by + 290, bx + 876, by + 290], fill="#DDDDDD")
    d.text((bx + 26, by + 304), "Назначение", font=font(14, bold=True), fill=TXT)
    d.text((bx + 26, by + 334), "Резервная копия на:", font=font(13), fill=TXT)
    d.ellipse([bx + 190, by + 334, bx + 204, by + 348], outline="#8A8A8A", fill=WHITE)
    d.ellipse([bx + 194, by + 338, bx + 200, by + 344], fill=SSMS)
    d.text((bx + 214, by + 330), "Диск", font=font(13), fill=TXT)
    d.ellipse([bx + 280, by + 334, bx + 294, by + 348], outline="#8A8A8A", fill=WHITE)
    d.text((bx + 304, by + 330), "Лента", font=font(13), fill=TXT)
    d.rectangle([bx + 26, by + 362, bx + 700, by + 490], fill=WHITE, outline="#B0B0B0")
    d.rectangle([bx + 27, by + 363, bx + 699, by + 387], fill="#EDEDED")
    d.text((bx + 36, by + 368), "Назначение", font=font(12, bold=True), fill=TXT)
    d.text((bx + 560, by + 368), "Свободно", font=font(12, bold=True), fill=TXT)
    d.rectangle([bx + 27, by + 388, bx + 699, by + 412], fill=SEL)
    d.text((bx + 36, by + 392), "D:\\Backup\\LibraryDB_full.bak", font=font(12), fill=TXT)
    d.text((bx + 560, by + 392), "84 ГБ", font=font(12), fill=TXT)
    mbutton(d, bx + 712, by + 388, 60, "…", h=26, size=12)
    mbutton(d, bx + 712, by + 362, 90, "Добавить", h=26, size=12)
    mbutton(d, bx + 712, by + 420, 90, "Удалить", h=26, size=12)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=by + 520)
    w.statusbar("LibraryDB   |   Модель восстановления: SIMPLE")
    w.save(os.path.join(OUT, "ssms_backup_dialog.png"))


def backup_options():
    w, ey = ssms("Microsoft SQL Server Management Studio — LibraryDB", show_query=False)
    d, box = win_modal(w, 900, 620, "Резервное копирование базы данных — LibraryDB",
                       y_off=-15)
    bx, by = box[0], box[1]
    tabs = ["Общие", "Параметры носителя", "Параметры резервного копирования",
            "Дополнительно"]
    tx = bx + 24
    for i, t in enumerate(tabs):
        tw = int(d.textlength(t, font=font(13))) + 24
        if i == 0:
            d.text((tx + 12, by + 54), t, font=font(13), fill=MUTED)
        elif i == 2:
            d.rectangle([tx, by + 46, tx + tw, by + 78], fill=WHITE)
            d.line([tx, by + 46, tx + tw, by + 46], fill=SSMS, width=2)
            d.text((tx + 12, by + 54), t, font=font(13, bold=True), fill=TXT)
        else:
            d.text((tx + 12, by + 54), t, font=font(13), fill=MUTED)
        tx += tw + 2
    d.line([bx + 24, by + 79, bx + 876, by + 79], fill="#C8C8C8")
    d.text((bx + 30, by + 96), "Перезаписать носитель", font=font(13, bold=True), fill=TXT)
    d.ellipse([bx + 30, by + 124, bx + 44, by + 138], outline="#8A8A8A", fill=WHITE)
    d.ellipse([bx + 34, by + 128, bx + 40, by + 134], fill=SSMS)
    d.text((bx + 54, by + 120), "Дописать к существующему набору носителей",
           font=font(13), fill=TXT)
    d.ellipse([bx + 30, by + 154, bx + 44, by + 168], outline="#8A8A8A", fill=WHITE)
    d.text((bx + 54, by + 150), "Перезаписать все существующие наборы носителей",
           font=font(13), fill=MUTED)
    d.text((bx + 54, by + 176), "(существующие резервные копии будут удалены — INIT)",
           font=font(11), fill=MUTED)
    d.text((bx + 30, by + 210), "Надежность", font=font(13, bold=True), fill=TXT)
    for i, (t, ch) in enumerate([("Проверить резервную копию после завершения", True),
                                 ("Выполнить проверку контрольной суммы перед записью "
                                  "на носитель и сохранить её", False)]):
        yy = by + 238 + i * 28
        d.rectangle([bx + 30, yy + 3, bx + 46, yy + 19], fill=ACCENT if ch else WHITE,
                    outline="#8A8A8A")
        if ch:
            d.line([bx + 34, yy + 11, bx + 37, yy + 15], fill=WHITE, width=2)
            d.line([bx + 37, yy + 15, bx + 43, yy + 7], fill=WHITE, width=2)
        d.text((bx + 56, yy), t, font=font(12), fill=TXT)
    d.text((bx + 30, by + 302), "Носитель резервной копии", font=font(13, bold=True), fill=TXT)
    d.ellipse([bx + 30, by + 334, bx + 44, by + 348], outline="#8A8A8A", fill=WHITE)
    d.ellipse([bx + 34, by + 338, bx + 40, by + 344], fill=SSMS)
    d.text((bx + 54, by + 330), "Диск", font=font(13), fill=TXT)
    d.ellipse([bx + 130, by + 334, bx + 144, by + 348], outline="#8A8A8A", fill=WHITE)
    d.text((bx + 154, by + 330), "Лента", font=font(13), fill=TXT)
    d.text((bx + 30, by + 366), "Имя носителя:", font=font(13), fill=TXT)
    text_field(d, bx + 160, by + 360, 340, "D:\\Backup\\LibraryDB_full.bak", 28, 12)
    d.text((bx + 30, by + 406), "Срок хранения (дней):", font=font(13), fill=TXT)
    text_field(d, bx + 240, by + 400, 120, "30", 28, 12)
    d.text((bx + 30, by + 446), "Параметры сжатия", font=font(13, bold=True), fill=TXT)
    d.ellipse([bx + 30, by + 474, bx + 44, by + 488], outline="#8A8A8A", fill=WHITE)
    d.text((bx + 54, by + 470), "По умолчанию для сервера", font=font(13), fill=TXT)
    d.ellipse([bx + 300, by + 474, bx + 314, by + 488], outline="#8A8A8A", fill=WHITE)
    d.ellipse([bx + 304, by + 478, bx + 310, by + 484], fill=SSMS)
    d.text((bx + 324, by + 470), "Сжать резервную копию", font=font(13), fill=TXT)
    d.text((bx + 540, by + 470), "2,1 : 1", font=font(12), fill=MUTED)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=by + 540)
    w.statusbar("LibraryDB   |   WITH INIT, COMPRESSION, CHECKSUM")
    w.save(os.path.join(OUT, "ssms_backup_options.png"))


def backup_success():
    w, ey = ssms("Microsoft SQL Server Management Studio — LibraryDB", show_query=False)
    d, box = win_modal(w, 640, 300, "Microsoft SQL Server Management Studio", y_off=0)
    bx, by = box[0], box[1]
    d.ellipse([bx + 28, by + 60, bx + 74, by + 106], fill="#E3F3E4")
    d.line([bx + 40, by + 84, bx + 48, by + 93], fill="#2E7D32", width=4)
    d.line([bx + 48, by + 93, bx + 62, by + 74], fill="#2E7D32", width=4)
    d.text((bx + 92, by + 58), "Резервное копирование базы данных «LibraryDB»",
           font=font(14, bold=True), fill=TXT)
    d.text((bx + 92, by + 84), "успешно завершено.", font=font(14, bold=True), fill=TXT)
    d.text((bx + 92, by + 116), "Файл: D:\\Backup\\LibraryDB_full.bak", font=font(12), fill=TXT)
    d.text((bx + 92, by + 140), "Размер: 48,6 МБ      Сжатие: 2,1 : 1", font=font(12),
           fill=MUTED)
    d.text((bx + 92, by + 164), "Дата и время: 06.11.2026 13:12:47", font=font(12),
           fill=MUTED)
    mbutton(d, bx + 480, by + 220, 120, "ОК", primary=True, h=32, size=13)
    w.statusbar("Резервное копирование базы данных успешно завершено", "LibraryDB")
    w.save(os.path.join(OUT, "ssms_backup_success.png"))


def restore_window():
    w, ey = ssms("Microsoft SQL Server Management Studio — LibraryDB", show_query=False)
    d, box = win_modal(w, 900, 600, "Восстановление базы данных — LibraryDB",
                       y_off=-10)
    bx, by = box[0], box[1]
    tabs = ["Общие", "Файлы", "Параметры восстановления"]
    tx = bx + 24
    for i, t in enumerate(tabs):
        tw = int(d.textlength(t, font=font(13))) + 24
        if i == 2:
            d.rectangle([tx, by + 46, tx + tw, by + 78], fill=WHITE)
            d.line([tx, by + 46, tx + tw, by + 46], fill=SSMS, width=2)
            d.text((tx + 12, by + 54), t, font=font(13, bold=True), fill=TXT)
        else:
            d.text((tx + 12, by + 54), t, font=font(13), fill=MUTED)
        tx += tw + 2
    d.line([bx + 24, by + 79, bx + 876, by + 79], fill="#C8C8C8")
    d.text((bx + 26, by + 96), "Параметры восстановления", font=font(14, bold=True), fill=TXT)
    d.ellipse([bx + 26, by + 126, bx + 40, by + 140], outline="#8A8A8A", fill=WHITE)
    d.ellipse([bx + 30, by + 130, bx + 36, by + 136], fill=SSMS)
    d.text((bx + 50, by + 122), "Перезаписать существующую базу данных (WITH REPLACE)",
           font=font(13), fill=TXT)
    d.text((bx + 26, by + 160), "Состояние восстановления:", font=font(13), bold=True, fill=TXT)
    for i, (t, sel) in enumerate([("RESTORE WITH RECOVERY", True),
                                  ("RESTORE WITH NORECOVERY", False),
                                  ("RESTORE WITH STANDBY", False)]):
        yy = by + 190 + i * 28
        d.ellipse([bx + 26, yy + 2, bx + 40, yy + 16], outline="#8A8A8A", fill=WHITE)
        if sel:
            d.ellipse([bx + 30, yy + 6, bx + 36, yy + 12], fill=SSMS)
        d.text((bx + 50, yy - 2), t, font=font(13), fill=TXT)
    d.text((bx + 26, by + 282), "Резервный набор для восстановления:", font=font(13),
           bold=True, fill=TXT)
    d.rectangle([bx + 26, by + 308, bx + 700, by + 420], fill=WHITE, outline="#B0B0B0")
    d.rectangle([bx + 27, by + 309, bx + 699, by + 333], fill="#EDEDED")
    for lab, cx in [("Восстановить", bx + 36), ("Тип", bx + 150), ("База данных", bx + 260),
                    ("Дата", bx + 420)]:
        d.text((cx, by + 314), lab, font=font(12, bold=True), fill=TXT)
    d.rectangle([bx + 27, by + 334, bx + 699, by + 358], fill=SEL)
    d.rectangle([bx + 34, by + 341, bx + 48, by + 355], fill=ACCENT)
    d.line([bx + 37, by + 348, bx + 40, by + 352], fill=WHITE, width=2)
    d.line([bx + 40, by + 352, bx + 45, by + 344], fill=WHITE, width=2)
    d.text((bx + 56, by + 338), "Полный", font=font(12), fill=TXT)
    d.text((bx + 150, by + 338), "Полная", font=font(12), fill=TXT)
    d.text((bx + 260, by + 338), "LibraryDB", font=font(12), fill=TXT)
    d.text((bx + 420, by + 338), "06.11.2026 13:12", font=font(12), fill=TXT)
    mbutton(d, bx + 712, by + 308, 160, "Проверить", h=28, size=12)
    mbutton(d, bx + 712, by + 344, 160, "Файл резервной копии…", h=28, size=12)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=by + 470)
    w.statusbar("LibraryDB   |   Восстановление из D:\\Backup\\LibraryDB_full.bak")
    w.save(os.path.join(OUT, "ssms_restore.png"))


def query_backup():
    w, ey = ssms("NGGTK-SQL\\SQLEXPRESS — Microsoft SQL Server Management Studio",
                 show_query=True, results=(
        ["USE master;",
         "GO",
         "BACKUP DATABASE LibraryDB",
         "TO DISK='D:\\Backup\\LibraryDB_full.bak'",
         "WITH INIT, COMPRESSION, CHECKSUM, STATS=10;",
         "GO",
         "-- Проверка созданной резервной копии",
         "RESTORE VERIFYONLY FROM DISK='D:\\Backup\\LibraryDB_full.bak';"],
        [("Результат"), ("Обработано 10 процентов."),
         ("Обработано 100 процентов."),
         ("Резервная копия базы данных успешно обработана: 948 страниц."),
         ("Резервный набор проверен: D:\\Backup\\LibraryDB_full.bak")]))
    w.statusbar("Запрос выполнен успешно   |   Время выполнения: 00:00:01,236",
                "NGGTK-SQL (15.0 RTM)")
    w.save(os.path.join(OUT, "ssms_query_backup.png"))


def backup_folder():
    w = Win(1280, 800, "Backup", margin=12,
            toolbar=["Создать", "Копировать", "Вставить", "Удалить", "Свойства",
                     "Упорядочить", "Просмотр"],
            status="3 элемента   |   1 элемент выбран   |   96,4 МБ")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill=WHITE)
    w.d.rounded_rectangle([x0 + 14, y0 + 8, x1 - 160, y0 + 34], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x0 + 22, y0 + 14, "Этот компьютер  >  Локальный диск (D:)  >  Backup",
           13, TXT)
    w.d.rounded_rectangle([x1 - 150, y0 + 8, x1 - 16, y0 + 34], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x1 - 140, y0 + 14, "Поиск: Backup", 12, MUTED)
    w.sidebar(x0 + 1, y0 + 44, 230, ["Рабочий стол", "Загрузки", "Документы",
                                     "Локальный диск (C:)", "Локальный диск (D:)",
                                     "USB (E:)", "Сеть"], active=4, title="НАВИГАЦИЯ")
    fy = y0 + 44
    w.d.line([x0 + 231, fy, x0 + 231, w.box[3] - 31], fill=LINE)
    w.d.rectangle([x0 + 232, fy, x1 - 1, fy + 26], fill="#F7F7F7")
    for lab, cx in [("Имя", x0 + 300), ("Дата изменения", x0 + 620), ("Тип", x0 + 840),
                    ("Размер", x0 + 1090)]:
        w.text(cx, fy + 5, lab, 12, MUTED)
    files = [("LibraryDB_full.bak", "06.11.2026 13:12", "Файл «BAK»", "48 624 КБ"),
             ("LibraryDB_log.trn", "06.11.2026 13:20", "Файл «TRN»", "12 802 КБ"),
             ("LibraryDB_diff.bak", "06.11.2026 13:18", "Файл «BAK»", "34 988 КБ")]
    ry = fy + 30
    for i, (n, dt, tp, sz) in enumerate(files):
        if i == 0:
            w.d.rectangle([x0 + 232, ry - 2, x1 - 2, ry + 26], fill=SEL)
        w.d.rounded_rectangle([x0 + 248, ry + 4, x0 + 268, ry + 22], radius=3, fill="#8C6D1F")
        w.text(x0 + 258, ry + 13, "B", 10, WHITE, bold=True, anchor="mm")
        w.text(x0 + 300, ry + 3, n, 13, TXT, bold=(i == 0))
        w.text(x0 + 620, ry + 3, dt, 13, TXT)
        w.text(x0 + 840, ry + 3, tp, 13, TXT)
        w.text(x0 + 1090, ry + 3, sz, 13, TXT)
        ry += 30
    w.statusbar("3 элемента   |   1 элемент выбран   |   96,4 МБ")
    w.save(os.path.join(OUT, "backup_folder.png"))


if __name__ == "__main__":
    connect_dialog()
    recovery_simple()
    backup_general()
    backup_options()
    backup_success()
    restore_window()
    query_backup()
    backup_folder()
