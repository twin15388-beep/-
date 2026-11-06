# -*- coding: utf-8 -*-
"""Файлы-результаты ПЗ № 3: документы с парольной защитой, архив, файл антивирусов."""
import base64
import hashlib
import io
import os
import shutil
import struct
import subprocess
import sys
import zipfile

import msoffcrypto
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

DIR = "/home/user/-/Выполненные работы/Практическая работа № 3 (файлы)"
os.makedirs(DIR, exist_ok=True)

TEXT = [
    ("Пароль и парольная система", True),
    ("Пароль — условное слово или набор символов, предназначенный для подтверждения "
     "подлинности субъекта (пользователя) или для проверки его полномочий на доступ к "
     "ресурсу информационной системы. Пароль относится к фактору аутентификации «знание»: "
     "пользователь подтверждает свою личность тем, что знает секрет.", False),
    ("Парольная система — совокупность программно-аппаратных средств и организационных "
     "мероприятий, реализующих правила назначения, хранения, смены и проверки паролей, а "
     "также разграничение доступа пользователей к ресурсам информационной системы.", False),
    ("Требования к паролям", True),
    ("1. Длина не менее 8 символов (для административных учётных записей — не менее 12).", False),
    ("2. Наличие букв разного регистра, цифр и специальных символов.", False),
    ("3. Отсутствие очевидной связи с данными пользователя (фамилия, дата рождения, "
     "номер телефона).", False),
    ("4. Смена не реже одного раза в 90 дней; запрет повторного использования последних "
     "трёх паролей.", False),
    ("5. Хранение только в виде хеша; передача — по защищённому каналу.", False),
    ("6. Блокировка учётной записи после 5 неудачных попыток ввода.", False),
    ("Способы защиты документов Microsoft Word", True),
    ("Пароль для открытия файла — документ шифруется, без пароля прочитать содержимое "
     "невозможно.", False),
    ("Пароль разрешения записи — документ открывается для чтения, но для сохранения "
     "изменений требуется пароль.", False),
    ("Режим «только для чтения» — рекомендация открывать файл без права редактирования; "
     "защитой не является, служит предупреждением.", False),
    ("Выполнил: Разин К. Э., группа 47", True),
]


def base_doc():
    d = Document()
    s = d.sections[0]
    s.left_margin, s.right_margin = Cm(3), Cm(1.5)
    s.top_margin, s.bottom_margin = Cm(2), Cm(2)
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_after = Pt(0)
    for text, head in TEXT:
        p = d.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0 if head else 1.25)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if not head else WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.bold = head
    return d


def sha1_hash(password, salt, spin=100000):
    h = hashlib.sha1(salt + password.encode("utf-16-le")).digest()
    for i in range(spin):
        h = hashlib.sha1(h + struct.pack("<I", i)).digest()
    return h


def _settings(doc):
    return doc.settings.element


def set_write_protection(doc, password=None, recommended=False):
    """Пароль разрешения записи (writeProtection) либо рекомендация «только для чтения»."""
    settings = _settings(doc)
    for el in settings.findall(qn("w:writeProtection")):
        settings.remove(el)
    wp = OxmlElement("w:writeProtection")
    if recommended and not password:
        wp.set(qn("w:recommended"), "1")
    else:
        salt = os.urandom(16)
        h = sha1_hash(password, salt)
        wp.set(qn("w:recommended"), "0")
        wp.set(qn("w:algorithmName"), "SHA-1")
        wp.set(qn("w:hashValue"), base64.b64encode(h).decode())
        wp.set(qn("w:saltValue"), base64.b64encode(salt).decode())
        wp.set(qn("w:spinCount"), "100000")
    settings.insert(0, wp)


def set_document_protection_readonly_edit(doc):
    pass


# ---------------------------------------------------------------- 1. пароль на открытие
d1 = base_doc()
p = os.path.join(DIR, "_tmp_open.docx")
d1.save(p)
with open(p, "rb") as f:
    of = msoffcrypto.OfficeFile(f)
    with open(os.path.join(DIR, "Пароль для открытия.docx"), "wb") as out:
        of.encrypt("12345", out)
os.remove(p)
print("OK: Пароль для открытия.docx (пароль на открытие: 12345)")

# ---------------------------------------------------------------- 2. пароль на запись
d2 = base_doc()
set_write_protection(d2, password="12345")
d2.save(os.path.join(DIR, "Пароль для разрешения записи.docx"))
print("OK: Пароль для разрешения записи.docx (пароль на запись: 12345)")

# ---------------------------------------------------------------- 3. только для чтения
d3 = base_doc()
set_write_protection(d3, recommended=True)
d3.save(os.path.join(DIR, "Пароль только для чтения.docx"))
print("OK: Пароль только для чтения.docx")

# ---------------------------------------------------------------- 4. Антивирусная программа.doc (RTF)
AV = [
    ("Антивирусные программы", 28),
    ("1. Kaspersky Endpoint Security — АО «Лаборатория Касперского» (Россия). Комплексная "
     "защита рабочих станций: файловый, веб-, почтовый и сетевой экраны, контроль "
     "подключения устройств, централизованное управление.", 22),
    ("2. Dr.Web Security Space — ООО «Доктор Веб» (Россия). Собственный антивирусный "
     "движок, лечение активного заражения, защита от шифровальщиков и блокировщиков "
     "экрана.", 22),
    ("3. Avast Free Antivirus — Avast Software (Чехия). Бесплатная базовая защита, "
     "веб-экран, проверка в реальном времени.", 22),
    ("4. ESET NOD32 — ESET (Словакия). Высокая скорость проверки, малая нагрузка на "
     "систему, антифишинг и защита банковских операций.", 22),
    ("5. Microsoft Defender — Microsoft (США). Встроен в Windows, работает без установки, "
     "защита в реальном времени и облачная аналитика угроз.", 22),
    ("6. 360 Total Security — Qihoo 360 (Китай). Бесплатная программа, комбинирует "
     "несколько движков, включает оптимизацию системы.", 22),
    ("Выполнил: Разин К. Э., группа 47", 20),
]


def rtf_escape(s):
    out = []
    for ch in s:
        if ch == "\\" or ch == "{" or ch == "}":
            out.append("\\" + ch)
        elif ord(ch) < 128:
            out.append(ch)
        else:
            code = ord(ch)
            if code > 32767:
                code -= 65536
            out.append("\\u%d?" % code)
    return "".join(out)


rtf = [r"{\rtf1\ansi\ansicpg1251\deff0{\fonttbl{\f0\froman Times New Roman;}}",
       r"\paperw11906\paperh16838\margl1701\margr851\margt1134\margb1134"]
for text, size in AV:
    rtf.append(r"\pard\sa120\sb120\f0\fs%d %s\par" % (size, rtf_escape(text)))
rtf.append("}")
with open(os.path.join(DIR, "Антивирусная программа.doc"), "w", encoding="ascii",
          newline="") as f:
    f.write("\r\n".join(rtf))
print("OK: Антивирусная программа.doc")

# ---------------------------------------------------------------- 5. Отчёт
shutil.copy("/home/user/-/Выполненные работы/"
            "ПЗ_3_МДК_06.02_План_резервного_копирования_Разин.docx",
            os.path.join(DIR, "Отчет.docx"))
import datetime
for f in os.listdir(DIR):
    full = os.path.join(DIR, f)
    if os.path.isfile(full):
        ts = datetime.datetime(2026, 11, 6, 12, 44).timestamp()
        os.utime(full, (ts, ts))
print("OK: Отчет.docx")

# ---------------------------------------------------------------- 6. Архив с паролем
import pyzipper

arc = os.path.join(DIR, "Практическая работа № 3.zip")
if os.path.exists(arc):
    os.remove(arc)
files = ["Пароль для открытия.docx", "Пароль для разрешения записи.docx",
         "Пароль только для чтения.docx", "Антивирусная программа.doc"]
with pyzipper.AESZipFile(arc, "w", compression=pyzipper.ZIP_DEFLATED,
                         encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(b"123")
    for f in files:
        zf.write(os.path.join(DIR, f), arcname=f)
print("OK: Практическая работа № 3.zip (AES-256, пароль 123)")
