# -*- coding: utf-8 -*-
"""Модуль оформления отчётов по практическим работам (ГОСТ-подобный стиль)."""
import os

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Times New Roman"
IMG_DIR = "/tmp/img"


def _set_cell_border(cell, sz=4):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tcPr.append(borders)


def _shade(cell, color="D9D9D9"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _no_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trPr.append(el)


class Report:
    """Документ отчёта с набором типовых элементов."""

    def __init__(self, work_no, mdk, title, student="Разин Константин Евгеньевич",
                 student_short="Разин К.Е.", group="47",
                 specialty="", teacher="", city_year="Новокуйбышевск, 2026"):
        self.doc = Document()
        self.fig_no = 0
        self.tab_no = 0
        self.work_no = work_no
        self.mdk = mdk
        self.title = title
        self.student = student
        self.student_short = student_short
        self.group = group
        self.specialty = specialty
        self.teacher = teacher
        self.city_year = city_year
        self._setup()

    # ------------------------------------------------------------------ setup
    def _setup(self):
        d = self.doc
        s = d.sections[0]
        s.page_width = Cm(21)
        s.page_height = Cm(29.7)
        s.left_margin = Cm(3)
        s.right_margin = Cm(1.5)
        s.top_margin = Cm(2)
        s.bottom_margin = Cm(2)
        s.header_distance = Cm(1.25)
        s.footer_distance = Cm(1.0)

        st = d.styles["Normal"]
        st.font.name = FONT
        st.font.size = Pt(14)
        st._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        st._element.rPr.rFonts.set(qn("w:cs"), FONT)
        pf = st.paragraph_format
        pf.line_spacing = 1.5
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.first_line_indent = Cm(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._add_page_numbers()

    def _add_page_numbers(self):
        footer = self.doc.sections[0].footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.font.name = FONT
        run.font.size = Pt(12)
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), "PAGE")
        r = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "24")
        rpr.append(sz)
        r.append(rpr)
        t = OxmlElement("w:t")
        t.text = "1"
        r.append(t)
        fld.append(r)
        p._p.append(fld)

    # ---------------------------------------------------------------- тексты
    def p(self, text="", indent=1.25, align="justify", bold=False, italic=False,
          size=14, space_after=0, space_before=0, line=1.5, color=None):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(indent)
        pf.line_spacing = line
        pf.space_after = Pt(space_after)
        pf.space_before = Pt(space_before)
        par.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                         "left": WD_ALIGN_PARAGRAPH.LEFT,
                         "center": WD_ALIGN_PARAGRAPH.CENTER,
                         "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
        if text:
            self._rich(par, text, size, bold, italic, color)
        return par

    def _rich(self, par, text, size=14, bold=False, italic=False, color=None):
        """Поддержка **жирного** внутри строки."""
        parts = text.split("**")
        for i, part in enumerate(parts):
            if not part:
                continue
            run = par.add_run(part)
            run.font.name = FONT
            run.font.size = Pt(size)
            run.bold = bold or (i % 2 == 1)
            run.italic = italic
            if color:
                run.font.color.rgb = RGBColor.from_string(color)
        return par

    def h1(self, text, page_break=False):
        if page_break:
            self.page_break()
        par = self.p(text.upper() if False else text, indent=0, align="center",
                     bold=True, space_before=12, space_after=12)
        par.paragraph_format.keep_with_next = True
        return par

    def h2(self, text):
        par = self.p(text, indent=1.25, align="justify", bold=True,
                     space_before=9, space_after=6)
        par.paragraph_format.keep_with_next = True
        return par

    def bullets(self, items, dash=True, indent=1.25):
        for it in items:
            par = self.p(("- " if dash else "") + it, indent=indent, align="justify")
        return None

    def num_list(self, items):
        for i, it in enumerate(items, 1):
            self.p(f"{i}) {it}", indent=1.25, align="justify")

    def code(self, lines, size=11):
        """Блок кода: монospace, светлая заливка, рамка."""
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.style = "Table Grid"
        cell = tbl.rows[0].cells[0]
        cell.text = ""
        _shade(cell, "F4F4F4")
        for i, line in enumerate(lines):
            par = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_after = Pt(1)
            par.paragraph_format.space_before = Pt(1)
            par.paragraph_format.first_line_indent = Cm(0)
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = par.add_run(line)
            run.font.name = "Consolas"
            run.font.size = Pt(size)
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        self.p("", indent=0, size=6, line=1.0)
        return tbl

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def spacer(self, n=1, size=14):
        for _ in range(n):
            par = self.doc.add_paragraph()
            par.paragraph_format.line_spacing = 1.0
            par.add_run("").font.size = Pt(size)

    # ------------------------------------------------------------ титульный
    def title_page(self, org_lines=None):
        org = org_lines or [
            "МИНИСТЕРСТВО ОБРАЗОВАНИЯ И НАУКИ САМАРСКОЙ ОБЛАСТИ",
            "Государственное автономное профессиональное образовательное учреждение",
            "Самарской области",
            "«Новокуйбышевский гуманитарно-технологический колледж»",
        ]
        for line in org:
            self.p(line, indent=0, align="center", size=12, bold=False, line=1.15)
        self.spacer(4)
        self.p("ОТЧЁТ", indent=0, align="center", bold=True, size=24, line=1.0)
        self.p(f"по практической работе № {self.work_no}", indent=0, align="center",
               bold=True, size=18, line=1.2)
        self.p(self.mdk, indent=0, align="center", size=14, line=1.2, space_after=6)
        self.spacer(1)
        self.p("Тема:", indent=0, align="center", bold=True, size=14)
        self.p(self.title, indent=0, align="center", bold=True, size=16, line=1.2)
        self.spacer(4)
        if self.specialty:
            self.p(self.specialty, indent=0, align="center", size=13)
        self.spacer(4)
        tbl = self.doc.add_table(rows=3, cols=2)
        tbl.autofit = False
        data = [("Выполнил:", f"студент группы {self.group}\n{self.student}"),
                ("Проверил:", self.teacher or "_______________________"),
                ("Оценка:", "_______________________")]
        for i, (a, b) in enumerate(data):
            c0, c1 = tbl.rows[i].cells
            c0.width = Cm(5.5)
            c1.width = Cm(9.5)
            p0 = c0.paragraphs[0]
            p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p0.paragraph_format.line_spacing = 1.0
            r = p0.add_run(a)
            r.font.name = FONT
            r.font.size = Pt(14)
            for j, line in enumerate(b.split("\n")):
                p1 = c1.paragraphs[0] if j == 0 else c1.add_paragraph()
                p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p1.paragraph_format.line_spacing = 1.0
                r = p1.add_run(line)
                r.font.name = FONT
                r.font.size = Pt(14)
        self.spacer(6)
        self.p(self.city_year, indent=0, align="center", size=14)
        self.page_break()

    # --------------------------------------------------------------- таблицы
    def table(self, header, rows, caption=None, widths=None, size=11,
              align_first_center=False, header_fill="D9D9D9", first_col_bold=False):
        if caption:
            self.tab_no += 1
            cp = self.p(f"Таблица {self.tab_no} – {caption}", indent=0, align="left",
                        size=12, italic=True, space_before=6, space_after=3)
            cp.paragraph_format.keep_with_next = True
        tbl = self.doc.add_table(rows=1, cols=len(header))
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        hdr = tbl.rows[0]
        _repeat_header(hdr)
        for i, h in enumerate(header):
            c = hdr.cells[i]
            c.text = ""
            par = c.paragraphs[0]
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_after = Pt(2)
            par.paragraph_format.space_before = Pt(2)
            r = par.add_run(h)
            r.font.name = FONT
            r.font.size = Pt(size)
            r.bold = True
            _shade(c, header_fill)
            _set_cell_border(c)
        for row in rows:
            cells = tbl.add_row().cells
            _no_split(tbl.rows[-1])
            for i, val in enumerate(row):
                c = cells[i]
                c.text = ""
                lines = str(val).split("\n")
                for j, line in enumerate(lines):
                    par = c.paragraphs[0] if j == 0 else c.add_paragraph()
                    par.paragraph_format.line_spacing = 1.0
                    par.paragraph_format.space_after = Pt(1)
                    par.paragraph_format.space_before = Pt(1)
                    par.paragraph_format.first_line_indent = Cm(0)
                    txt = line
                    if txt.startswith("- "):
                        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        par.paragraph_format.left_indent = Cm(0.3)
                    elif align_first_center and i == 0:
                        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif len(txt) < 18 and i > 0 and len(row) > 2:
                        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    parts = txt.split("**")
                    for k, part in enumerate(parts):
                        if not part:
                            continue
                        r = par.add_run(part)
                        r.font.name = FONT
                        r.font.size = Pt(size)
                        r.bold = (k % 2 == 1) or (first_col_bold and i == 0)
                _set_cell_border(c)
        if widths:
            for i, w in enumerate(widths):
                for row in tbl.rows:
                    row.cells[i].width = Cm(w)
        self.p("", indent=0, size=6, line=1.0)
        return tbl

    # --------------------------------------------------------------- рисунки
    def figure(self, path, width_cm=15.5, caption=None, align="center"):
        par = self.doc.add_paragraph()
        par.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER,
                         "left": WD_ALIGN_PARAGRAPH.LEFT}[align]
        par.paragraph_format.first_line_indent = Cm(0)
        par.paragraph_format.space_before = Pt(6)
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.line_spacing = 1.0
        par.paragraph_format.keep_with_next = True
        par.add_run().add_picture(path, width=Cm(width_cm))
        if caption:
            self.fig_no += 1
            self.p(f"Рисунок {self.fig_no} – {caption}", indent=0, align="center",
                   size=12, italic=True, space_after=8, line=1.0)
        return self.fig_no

    # ---------------------------------------------------------------- финал
    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.doc.save(path)
        print("OK:", path)
        return path
