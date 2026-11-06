# -*- coding: utf-8 -*-
"""Иллюстрации к ПЗ № 3 (МДК 06.02): парольная защита, архивация, антивирус."""
import os

from PIL import ImageDraw

from mockui import (ACCENT, LINE, MUTED, SEL, TXT, WHITE, Win, dialog_buttons,
                    font, str_list, text_field, win_modal)

OUT = "/tmp/img/pz3"
os.makedirs(OUT, exist_ok=True)


# --------------------------------------------------------------- Word: пароль
def word_password():
    w = Win(1250, 800, "Пароль для открытия.docx — Word", margin=12,
            toolbar=["Файл", "Главная", "Вставка", "Рисование", "Дизайн", "Макет",
                     "Ссылки", "Рассылки", "Рецензирование", "Вид", "Справка"],
            status="Стр. 1 из 1   |   128 слов   |   RU")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 30], fill="#8E9BA8")
    # лента команд
    w.d.rectangle([x0 + 1, y0, x1 - 1, y0 + 40], fill="#FAFAFA")
    w.d.line([x0 + 1, y0 + 40, x1 - 1, y0 + 40], fill="#DDDDDD")
    w.text(x0 + 20, y0 + 12, "Calibri (Основной)   14", 13, TXT)
    w.text(x0 + 260, y0 + 12, "Ж  К  Ч   ≡   x²   Aa", 13, TXT)
    w.text(x1 - 220, y0 + 12, "Стили   Найти   Заменить", 13, MUTED)
    y0 = y0 + 44
    # «лист» документа
    pw = 720
    px = (x0 + x1 - pw) // 2
    w.d.rectangle([px, y0 + 18, px + pw, w.box[3] - 46], fill="#FFFFFF")
    w.text(px + 60, y0 + 44, "Пароль и парольная система", 17, TXT, bold=True)
    lines = [
        "**Пароль** — это условное слово или набор символов, предназначенный для",
        "подтверждения подлинности субъекта (пользователя) или для проверки",
        "полномочий на доступ к ресурсу информационной системы.",
        "",
        "**Парольная система** — совокупность программно-аппаратных средств и",
        "организационных мероприятий, реализующих правила назначения, хранения,",
        "смены и проверки паролей, а также разграничение доступа пользователей",
        "к ресурсам информационной системы.",
        "",
        "Основные требования к паролям: длина не менее 8 символов, наличие букв",
        "разного регистра, цифр и специальных символов, отсутствие очевидных",
        "связей с данными пользователя, регулярная смена (не реже 1 раза в 90 дней).",
    ]
    yy = y0 + 80
    for ln in lines:
        if not ln:
            yy += 16
            continue
        f = font(13)
        w.text(px + 60, yy, ln, 13, TXT)
        yy += 24
    d, box = win_modal(w, 620, 430, "Общие параметры", y_off=10)
    bx, by = box[0], box[1]
    d.text((bx + 26, by + 58), "Параметры файла", font=font(14, bold=True), fill=TXT)
    d.text((bx + 26, by + 92), "Имя файла:", font=font(13), fill=TXT)
    d.text((bx + 210, by + 92), "Пароль для открытия.docx", font=font(13), fill=MUTED)
    d.text((bx + 26, by + 122), "Расположение:", font=font(13), fill=TXT)
    d.text((bx + 210, by + 122), "D:\\Практическая работа № 3", font=font(13), fill=MUTED)
    d.text((bx + 26, by + 168), "Пароль для открытия файла:", font=font(13), fill=TXT)
    text_field(d, bx + 26, by + 192, 300, "••••••••", 30, 14)
    d.text((bx + 26, by + 234), "Пароль разрешения записи:", font=font(13), fill=TXT)
    text_field(d, bx + 26, by + 258, 300, "", 30, 14, placeholder="(не задан)")
    d.rectangle([bx + 26, by + 302, bx + 42, by + 318], outline="#8A8A8A", fill=WHITE)
    d.line([bx + 29, by + 310, bx + 32, by + 314], fill=TXT, width=2)
    d.line([bx + 32, by + 314, bx + 39, by + 304], fill=TXT, width=2)
    d.text((bx + 52, by + 300), "Рекомендовать доступ только для чтения",
           font=font(13), fill=TXT)
    d.text((bx + 26, by + 336), "Пароль применяется при сохранении файла "
           "(кнопка «Сохранить»).", font=font(12), fill=MUTED)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=by + 372)
    w.save(os.path.join(OUT, "word_password.png"))


def word_readonly():
    w = Win(1250, 800, "Пароль только для чтения — Word", margin=12,
            toolbar=["Файл", "Главная", "Вставка", "Рецензирование", "Вид"],
            status="Только чтение   |   Стр. 1 из 1")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, y0 + 46], fill="#FDF6E3")
    pass
    w.d.rectangle([x0 + 1, y0 + 46, x1 - 1, w.box[3] - 30], fill="#8E9BA8")
    w.text(x0 + 24, y0 + 13, "РЕЖИМ ОГРАНИЧЕННОГО ФУНКЦИОНИРОВАНИЯ", 13, "#7A5A00",
           bold=True)
    w.text(x1 - 24, y0 + 13, "Разрешить редактирование", 13, ACCENT, anchor="ra")
    pw = 700
    px = (x0 + x1 - pw) // 2
    w.d.rectangle([px, y0 + 66, px + pw, w.box[3] - 46], fill="#FFFFFF")
    w.text(px + 55, y0 + 92, "Пароль только для чтения", 17, TXT, bold=True)
    txt = "Документ открыт в режиме «только для чтения», поскольку при сохранении "
    w.text(px + 55, y0 + 130, "установлен флажок «Рекомендовать доступ только для", 13, TXT)
    w.text(px + 55, y0 + 154, "чтения». Любые изменения невозможно сохранить в этот", 13, TXT)
    w.text(px + 55, y0 + 178, "файл — только в новую копию.", 13, TXT)
    w.d.rectangle([px + 55, y0 + 216, px + pw - 55, y0 + 300], fill="#F4F7FB",
                  outline="#C9D6E3")
    w.text(px + 70, y0 + 228, "Файл: D:\\Практическая работа № 3\\Пароль только для чтения.docx",
           12, TXT)
    w.text(px + 70, y0 + 250, "Свойства: только чтение (флаг «Рекомендовать доступ "
           "только для чтения»)", 12, TXT)
    w.text(px + 70, y0 + 272, "Автор: Разин К. Э., группа 47", 12, MUTED)
    w.save(os.path.join(OUT, "word_readonly.png"))


# ------------------------------------------------------------------- WinRAR
def winrar():
    w = Win(1250, 800, "Практическая работа № 3 — WinRAR", margin=12,
            toolbar=["Файл", "Команды", "Избранное", "Параметры", "Справка"],
            status="6 объектов   |   198 720 байт   |   Свободно 84,2 ГБ")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    # адресная строка
    w.d.rounded_rectangle([x0 + 12, y0 + 8, x1 - 12, y0 + 36], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x0 + 20, y0 + 15, "D:\\Практическая работа № 3\\", 13, TXT)
    w.text(x0 + 210, y0 + 15, "☰", 13, MUTED)
    fy = y0 + 42
    w.d.rectangle([x0 + 1, fy, x1 - 1, w.box[3] - 30], fill=WHITE)
    # заголовки колонок
    w.d.rectangle([x0 + 1, fy, x1 - 1, fy + 26], fill="#F0F0F0")
    for label, cx in [("Имя", x0 + 34), ("Размер", x0 + 430), ("Упакован", x0 + 530),
                      ("Тип", x0 + 630), ("Изменён", x0 + 760), ("CRC32", x0 + 900)]:
        w.text(cx, fy + 5, label, 13, TXT, bold=True)
    files = [("..", "<Папка>", "", "", "06.11.2026 12:31", ""),
             ("Пароль для открытия.docx", "24 118", "7 940", "Файл «docx»", "06.11.2026 12:18", "A41F09C2"),
             ("Пароль для разрешения записи.docx", "23 904", "7 812", "Файл «docx»", "06.11.2026 12:21", "5C1B77AE"),
             ("Пароль только для чтения.docx", "22 640", "7 205", "Файл «docx»", "06.11.2026 12:24", "D9030E14"),
             ("Антивирусная программа.doc", "31 208", "9 118", "Файл «doc»", "06.11.2026 12:29", "77AA21F0"),
             ("Практическая работа № 3.zip", "26 771", "26 771", "Сжатая ZIP-папка", "06.11.2026 12:44", "1E4C88B7")]
    ry = fy + 28
    for i, (n, sz, pk, tp, dt, crc) in enumerate(files):
        if i == 4:
            w.d.rectangle([x0 + 1, ry - 2, x1 - 1, ry + 22], fill=SEL)
        w.d.rounded_rectangle([x0 + 12, ry + 3, x0 + 26, ry + 17], radius=2,
                              fill="#2B579A" if n.endswith("docx") else
                              ("#3B6EA5" if n.endswith(".doc") else "#B03030"))
        w.fit(x0 + 34, ry, n, 380, 13, TXT)
        w.text(x0 + 430, ry, sz, 13, TXT)
        w.text(x0 + 530, ry, pk, 13, TXT)
        w.text(x0 + 630, ry, tp, 13, TXT)
        w.text(x0 + 760, ry, dt, 13, TXT)
        w.text(x0 + 900, ry, crc, 13, MUTED, mono=True)
        ry += 24
    d, box = win_modal(w, 700, 500, "Имя и параметры архива", y_off=0)
    bx, by = box[0], box[1]
    d.text((bx + 24, by + 56), "Архив:", font=font(14, bold=True), fill=TXT)
    text_field(d, bx + 24, by + 78, 650, "Практическая работа № 3.zip", 30, 14)
    # вкладки
    tabs = ["Общие", "Дополнительно", "Комментарий", "Опции"]
    tx = bx + 24
    for i, t in enumerate(tabs):
        tw = int(d.textlength(t, font=font(13))) + 24
        if i == 1:
            d.rounded_rectangle([tx, by + 122, tx + tw, by + 148], radius=4, fill=WHITE,
                                outline="#BDBDBD")
            d.text((tx + 12, by + 127), t, font=font(13, bold=True), fill=TXT)
        else:
            d.text((tx + 12, by + 127), t, font=font(13), fill=MUTED)
        tx += tw + 4
    d.line([bx + 24, by + 149, bx + 674, by + 149], fill="#BDBDBD")
    d.text((bx + 24, by + 166), "Формат архива:", font=font(13), fill=TXT)
    d.text((bx + 570, by + 166), "ZIP (AES-256)", font=font(13, bold=True), fill=TXT)
    d.text((bx + 24, by + 200), "Метод сжатия:", font=font(13), fill=TXT)
    d.text((bx + 610, by + 200), "Обычный", font=font(13, bold=True), fill=TXT)
    # чекбокс с паролем
    d.rectangle([bx + 24, by + 240, bx + 41, by + 257], fill=ACCENT, outline="#8A8A8A")
    d.line([bx + 28, by + 249, bx + 31, by + 253], fill=WHITE, width=2)
    d.line([bx + 31, by + 253, bx + 38, by + 243], fill=WHITE, width=2)
    d.text((bx + 50, by + 238), "Установить пароль", font=font(13), fill=TXT)
    d.text((bx + 24, by + 280), "Введите пароль:", font=font(13), fill=TXT)
    text_field(d, bx + 24, by + 304, 260, "123", 30, 14, mono=True)
    d.text((bx + 300, by + 280), "Повторите ввод:", font=font(13), fill=TXT)
    text_field(d, bx + 300, by + 304, 260, "123", 30, 14, mono=True)
    d.text((bx + 24, by + 352), "Пароль будет запрошен при распаковке архива.",
           font=font(12), fill=MUTED)
    dialog_buttons(d, box, ("ОК", "Отмена"), y=by + 440)
    w.statusbar("6 объектов   |   198 720 байт   |   Свободно 84,2 ГБ")
    w.save(os.path.join(OUT, "winrar_archive.png"))


# ------------------------------------------------------------------ антивирус
def antivirus_main():
    w = Win(1250, 800, "Антивирус — главное окно", margin=12,
            tabs=["Главная", "Проверка", "Обновление", "Карантин", "Журнал", "Параметры"],
            status="Базы обновлены: 06.11.2026 10:24   |   Лицензия: 214 дней")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F4F6F9")
    # статус
    w.panel(x0 + 20, y0 + 18, 380, 300)
    w.d.ellipse([x0 + 160, y0 + 44, x0 + 240, y0 + 124], fill="#E3F3E4")
    w.d.ellipse([x0 + 178, y0 + 62, x0 + 222, y0 + 106], fill="#2E7D32")
    w.d.line([x0 + 190, y0 + 84, x0 + 198, y0 + 93], fill=WHITE, width=4)
    w.d.line([x0 + 198, y0 + 93, x0 + 212, y0 + 74], fill=WHITE, width=4)
    w.text(x0 + 210, y0 + 142, "Компьютер защищён", 18, TXT, bold=True, anchor="ma")
    w.text(x0 + 210, y0 + 172, "Активных угроз не обнаружено", 13, MUTED, anchor="ma")
    w.button(x0 + 60, y0 + 206, 300, "Выполнить быструю проверку", primary=True, h=32, size=13)
    w.button(x0 + 130, y0 + 250, 160, "Обновить базы", h=32, size=13)
    # сводка справа
    w.panel(x0 + 420, y0 + 18, 800, 300)
    w.text(x0 + 440, y0 + 32, "Состояние защиты", 15, TXT, bold=True)
    rows = [("Дата и время выпуска антивирусных баз", "06.11.2026 10:24"),
            ("Дата и время последней быстрой проверки", "05.11.2026 11:00"),
            ("Дата и время последней полной проверки", "01.11.2026 02:00"),
            ("Объектов на карантине", "3"),
            ("Файлов, добавленных в исключения", "4"),
            ("Модули защиты", "Файловый, Веб, Почтовый, Сетевой экран"),
            ("Автозапуск при старте системы", "включён")]
    yy = y0 + 64
    for k, v in rows:
        w.text(x0 + 440, yy, k, 13, MUTED)
        w.text(x0 + 830, yy, v, 13, TXT, bold=True)
        w.d.line([x0 + 440, yy + 22, x1 - 20, yy + 22], fill="#EDEDED")
        yy += 32
    # вкладка «Карантин» — список объектов
    w.panel(x0 + 20, y0 + 336, 1200, 300)
    w.text(x0 + 40, y0 + 350, "Карантин и журнал обнаружений", 15, TXT, bold=True)
    w.text(x0 + 900, y0 + 350, "Показано 3 объекта", 12, MUTED)
    hy = y0 + 382
    w.d.rectangle([x0 + 30, hy, x1 - 30, hy + 26], fill="#EDF1F6")
    for lab, cx in [("Объект", x0 + 40), ("Угроза", x0 + 520), ("Статус", x0 + 800),
                    ("Дата помещения", x0 + 960)]:
        w.text(cx, hy + 5, lab, 13, TXT, bold=True)
    q = [("C:\\Users\\Student\\Downloads\\setup_install.exe", "Trojan.Win32.Agent.qwe",
          "На карантине", "03.11.2026 09:14"),
         ("D:\\Практическая работа № 3\\scan.tmp", "EICAR-Test-File", "На карантине",
          "04.11.2026 14:37"),
         ("E:\\архив фотографий\\foto_setup.exe", "Worm.Win32.AutoRun.kj", "На карантине",
          "05.11.2026 10:52")]
    ry = hy + 30
    for i, (o, thr, st, dt) in enumerate(q):
        if i == 1:
            w.d.rectangle([x0 + 31, ry - 2, x1 - 31, ry + 24], fill=SEL)
        w.fit(x0 + 40, ry + 2, o, 460, 12, TXT)
        w.fit(x0 + 520, ry + 2, thr, 260, 12, "#B03030")
        w.text(x0 + 800, ry + 2, st, 12, TXT)
        w.text(x0 + 960, ry + 2, dt, 12, MUTED)
        ry += 28
    w.text(x0 + 40, y0 + 500, "Действия:  Восстановить   |   Удалить   |   Отправить "
           "в лабораторию", 12, MUTED)
    w.statusbar("Базы обновлены: 06.11.2026 10:24   |   Лицензия: 214 дней")
    w.save(os.path.join(OUT, "antivirus_main.png"))


def antivirus_quarantine():
    w = Win(1250, 800, "Антивирус — Карантин", margin=12,
            tabs=["Главная", "Проверка", "Обновление", "Карантин", "Журнал", "Параметры"],
            status="Объектов на карантине: 3   |   Занято: 1,4 МБ")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F4F6F9")
    w.panel(x0 + 20, y0 + 18, 1200, 700)
    w.text(x0 + 40, y0 + 34, "Карантин", 18, TXT, bold=True)
    w.text(x0 + 40, y0 + 66, "Подозрительные объекты изолированы и не могут "
           "нанести вред системе", 13, MUTED)
    w.button(x0 + 40, y0 + 96, 150, "Восстановить", h=30)
    w.button(x0 + 200, y0 + 96, 120, "Удалить", h=30)
    w.button(x0 + 330, y0 + 96, 200, "Отправить в лабораторию", h=30)
    hy = y0 + 142
    w.d.rectangle([x0 + 40, hy, x1 - 40, hy + 28], fill="#EDF1F6")
    cols = [("Объект", x0 + 52), ("Угроза", x0 + 470), ("Размер", x0 + 780),
            ("Статус", x0 + 880), ("Дата", x0 + 1010)]
    for lab, cx in cols:
        w.text(cx, hy + 6, lab, 13, TXT, bold=True)
    q = [("setup_install.exe", "Trojan.Win32.Agent.qwe", "612 КБ", "Карантин",
          "03.11.2026"),
         ("scan.tmp", "EICAR-Test-File", "68 Б", "Карантин", "04.11.2026"),
         ("foto_setup.exe", "Worm.Win32.AutoRun.kj", "824 КБ", "Карантин", "05.11.2026")]
    ry = hy + 32
    for i, (o, thr, sz, st, dt) in enumerate(q):
        if i == 0:
            w.d.rectangle([x0 + 41, ry - 2, x1 - 41, ry + 24], fill=SEL)
        w.text(x0 + 52, ry + 2, o, 12, TXT)
        w.text(x0 + 470, ry + 2, thr, 12, "#B03030")
        w.text(x0 + 780, ry + 2, sz, 12, TXT)
        w.text(x0 + 880, ry + 2, st, 12, TXT)
        w.text(x0 + 1010, ry + 2, dt, 12, MUTED)
        w.d.line([x0 + 41, ry + 26, x1 - 41, ry + 26], fill="#EDEDED")
        ry += 30
    w.statusbar("Объектов на карантине: 3   |   Занято: 1,4 МБ")
    w.save(os.path.join(OUT, "antivirus_quarantine.png"))


def antivirus_schedule():
    w = Win(1250, 800, "Антивирус — Параметры: запланированные проверки", margin=12,
            tabs=["Главная", "Проверка", "Обновление", "Карантин", "Журнал", "Параметры"],
            status="Изменения сохранены")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F4F6F9")
    w.sidebar(x0 + 1, y0, 300, ["Общие", "Защита", "Проверка", "Обновление",
                                "Запланированные проверки", "Уведомления",
                                "Исключения"], active=4, title="ПАРАМЕТРЫ")
    w.text(x0 + 330, y0 + 24, "Запланированные проверки", 18, TXT, bold=True)
    w.text(x0 + 330, y0 + 58, "Проверка запускается автоматически в указанное "
           "время по расписанию", 13, MUTED)
    w.panel(x0 + 330, y0 + 92, 890, 252)
    hy = y0 + 104
    w.d.rectangle([x0 + 340, hy, x1 - 30, hy + 28], fill="#EDF1F6")
    for lab, cx in [("Задача", x0 + 352), ("Тип проверки", x0 + 540),
                    ("День", x0 + 700), ("Время", x0 + 810), ("Состояние", x0 + 900)]:
        w.text(cx, hy + 6, lab, 13, TXT, bold=True)
    tasks = [("Проверка № 1", "Быстрая", "Понедельник", "11:00", "Включена"),
             ("Проверка № 2", "Полная", "Суббота", "02:00", "Включена"),
             ("Съёмные носители", "При подключении", "—", "—", "Включена")]
    ry = hy + 32
    for i, (a, b, c, e, f) in enumerate(tasks):
        if i == 0:
            w.d.rectangle([x0 + 331, ry - 3, x1 - 31, ry + 25], fill=SEL)
        w.text(x0 + 352, ry + 2, a, 13, TXT, bold=(i == 0))
        w.text(x0 + 540, ry + 2, b, 13, TXT)
        w.text(x0 + 700, ry + 2, c, 13, TXT)
        w.text(x0 + 810, ry + 2, e, 13, TXT)
        w.text(x0 + 900, ry + 2, f, 13, "#2E7D32")
        ry += 34
    w.button(x0 + 330, y0 + 356, 130, "Добавить", primary=True, h=32)
    w.button(x0 + 470, y0 + 356, 170, "Изменить", h=32)
    w.button(x0 + 650, y0 + 356, 120, "Удалить", h=32)
    # панель настройки выбранной задачи
    w.panel(x0 + 330, y0 + 402, 890, 236)
    w.text(x0 + 350, y0 + 414, "Настройка задачи «Проверка № 1»", 14, TXT, bold=True)
    w.text(x0 + 350, y0 + 448, "Периодичность:", 13, TXT)
    xx = x0 + 350 + 120
    for t, sel in [("Ежедневно", False), ("Еженедельно", True), ("Ежемесячно", False)]:
        xx = w.radio(xx, y0 + 448, t, sel, 13) + 20
    w.text(x0 + 350, y0 + 486, "День недели:", 13, TXT)
    w.d.rounded_rectangle([x0 + 470, y0 + 480, x0 + 670, y0 + 510], radius=4, fill=WHITE,
                          outline="#B6B6B6")
    w.text(x0 + 480, y0 + 486, "Понедельник", 13, TXT)
    w.text(x0 + 654, y0 + 485, "v", 11, MUTED)
    w.text(x0 + 700, y0 + 486, "Время запуска:", 13, TXT)
    w.d.rounded_rectangle([x0 + 820, y0 + 480, x0 + 930, y0 + 510], radius=4, fill=WHITE,
                          outline="#B6B6B6")
    w.text(x0 + 830, y0 + 486, "11:00", 13, TXT)
    w.text(x0 + 914, y0 + 485, "v", 11, MUTED)
    w.checkbox(x0 + 350, y0 + 528, "Запускать пропущенную проверку при включении компьютера", True, 13)
    w.checkbox(x0 + 350, y0 + 560, "Завершать работу компьютера после проверки", False, 13)
    w.checkbox(x0 + 350, y0 + 592, "Проверять архивы и съёмные носители", True, 13)
    w.statusbar("Изменения сохранены")
    w.save(os.path.join(OUT, "antivirus_schedule.png"))


def antivirus_scan():
    w = Win(1250, 800, "Антивирус — Проверка съёмного носителя", margin=12,
            tabs=["Главная", "Проверка", "Обновление", "Карантин", "Журнал", "Параметры"],
            status="Проверка завершена: 06.11.2026 12:41")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill="#F4F6F9")
    w.panel(x0 + 20, y0 + 18, 1200, 250)
    w.text(x0 + 44, y0 + 34, "Проверка съёмного носителя «USB (E:)»", 17, TXT, bold=True)
    w.text(x0 + 44, y0 + 68, "Проверено объектов: 12 483   |   Обнаружено угроз: 2   |   "
           "Обработано: 2", 13, MUTED)
    # прогресс
    w.d.rounded_rectangle([x0 + 44, y0 + 104, x1 - 44, y0 + 128], radius=8, fill="#E3E7ED")
    w.d.rounded_rectangle([x0 + 44, y0 + 104, x0 + 44 + 1240, y0 + 128], radius=8,
                          fill="#2E7D32")
    w.text(x0 + 44, y0 + 140, "100 %  —  проверка завершена", 13, "#2E7D32", bold=True)
    w.text(x0 + 44, y0 + 172, "Текущий объект: E:\\Музыка\\track_07.mp3", 13, MUTED)
    w.button(x0 + 44, y0 + 206, 170, "Проверить снова", h=32)
    w.button(x0 + 228, y0 + 206, 150, "Отчёт", h=32)
    w.button(x0 + 392, y0 + 206, 150, "Закрыть", h=32)
    # результаты
    w.panel(x0 + 20, y0 + 286, 1200, 420)
    w.text(x0 + 44, y0 + 302, "Результаты проверки", 15, TXT, bold=True)
    hy = y0 + 336
    w.d.rectangle([x0 + 34, hy, x1 - 34, hy + 26], fill="#EDF1F6")
    for lab, cx in [("Файл", x0 + 44), ("Угроза", x0 + 560), ("Действие", x0 + 800),
                    ("Статус", x0 + 990)]:
        w.text(cx, hy + 5, lab, 13, TXT, bold=True)
    res = [("E:\\autorun.inf", "Worm.Win32.AutoRun.kj", "Помещён в карантин", "Выполнено"),
           ("E:\\Музыка\\foto_setup.exe", "Trojan.Win32.Agent.qwe", "Удалён", "Выполнено"),
           ("E:\\Документы\\отчёт.docx", "—", "Проверен", "Чисто"),
           ("E:\\Документы\\смета.xlsx", "—", "Проверен", "Чисто"),
           ("E:\\Фото\\IMG_2041.jpg", "—", "Проверен", "Чисто")]
    ry = hy + 32
    for i, (f, thr, act, st) in enumerate(res):
        if i == 0:
            w.d.rectangle([x0 + 35, ry - 3, x1 - 35, ry + 24], fill=SEL)
        w.fit(x0 + 44, ry + 2, f, 500, 12, TXT)
        w.fit(x0 + 560, ry + 2, thr, 220, 12, "#B03030" if thr != "—" else MUTED)
        w.text(x0 + 800, ry + 2, act, 12, TXT)
        w.text(x0 + 990, ry + 2, st, 12, "#2E7D32" if st == "Выполнено" else MUTED)
        ry += 30
    w.statusbar("Проверка завершена: 06.11.2026 12:41")
    w.save(os.path.join(OUT, "antivirus_scan.png"))


def explorer_folder():
    w = Win(1250, 800, "Практическая работа № 3", margin=12,
            toolbar=["Создать", "Копировать", "Вставить", "Удалить", "Свойства",
                     "Упорядочить", "Просмотр"],
            status="6 элементов   |   1 элемент выбран   |   128 КБ")
    x0, y0, x1 = w.x0, w.cy0, w.x1
    w.d.rectangle([x0 + 1, y0, x1 - 1, w.box[3] - 31], fill=WHITE)
    # адресная строка
    w.d.rounded_rectangle([x0 + 14, y0 + 8, x1 - 160, y0 + 34], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x0 + 22, y0 + 14, "Этот компьютер  >  Локальный диск (D:)  >  "
           "Практическая работа № 3", 13, TXT)
    w.d.rounded_rectangle([x1 - 150, y0 + 8, x1 - 16, y0 + 34], radius=3, fill=WHITE,
                          outline="#C6C6C6")
    w.text(x1 - 140, y0 + 14, "Поиск: Практическая…", 12, MUTED)
    # боковая панель
    w.sidebar(x0 + 1, y0 + 44, 230, ["Рабочий стол", "Загрузки", "Документы",
                                     "Изображения", "Музыка", "Видео",
                                     "Локальный диск (C:)", "Локальный диск (D:)",
                                     "USB (E:)", "Сеть"], active=7, title="НАВИГАЦИЯ")
    fy = y0 + 44
    w.d.line([x0 + 231, fy, x0 + 231, w.box[3] - 31], fill=LINE)
    w.d.rectangle([x0 + 232, fy, x1 - 1, fy + 26], fill="#F7F7F7")
    for lab, cx in [("Имя", x0 + 300), ("Дата изменения", x0 + 620), ("Тип", x0 + 830),
                    ("Размер", x0 + 1090)]:
        w.text(cx, fy + 5, lab, 12, MUTED)
    files = [("Отчет.docx", "06.11.2026 12:44", "Документ Word", "1 842 КБ", "#2B579A", "W"),
             ("Пароль для открытия.docx", "06.11.2026 12:18", "Документ Word", "24 КБ", "#2B579A", "W"),
             ("Пароль для разрешения записи.docx", "06.11.2026 12:21", "Документ Word", "23 КБ", "#2B579A", "W"),
             ("Пароль только для чтения.docx", "06.11.2026 12:24", "Документ Word", "22 КБ", "#2B579A", "W"),
             ("Практическая работа № 3.zip", "06.11.2026 12:44", "Сжатая ZIP-папка", "110 КБ", "#8C6D1F", "Z"),
             ("Антивирусная программа.doc", "06.11.2026 12:29", "Документ Word 97-2003", "31 КБ", "#2B579A", "W")]
    ry = fy + 30
    for i, (n, dt, tp, sz, col, l) in enumerate(files):
        if i == 4:
            w.d.rectangle([x0 + 232, ry - 2, x1 - 2, ry + 26], fill=SEL)
        w.d.rounded_rectangle([x0 + 248, ry + 4, x0 + 268, ry + 22], radius=3, fill=col)
        w.text(x0 + 258, ry + 13, l, 10, WHITE, bold=True, anchor="mm")
        w.fit(x0 + 300, ry + 3, n, 300, 13, TXT, bold=(i == 4))
        w.text(x0 + 620, ry + 3, dt, 13, TXT)
        w.fit(x0 + 830, ry + 3, tp, 240, 13, TXT)
        w.text(x0 + 1090, ry + 3, sz, 13, TXT)
        ry += 30
    w.statusbar("6 элементов   |   1 элемент выбран   |   128 КБ")
    w.save(os.path.join(OUT, "explorer_folder.png"))


if __name__ == "__main__":
    word_password()
    word_readonly()
    winrar()
    antivirus_main()
    antivirus_quarantine()
    antivirus_schedule()
    antivirus_scan()
    explorer_folder()
