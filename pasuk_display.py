import tkinter as tk
from tkinter import font as tkfont

from theme import ROOT_BG_COLOR, NAVY_COLOR, MUTED_TEXT_COLOR, hebrew_font_family
from drawing import fit_font_size

# Shema (Devarim 6:4) with nikkud only — no te'amim.
SAMPLE_PASUK = "שְׁמַע יִשְׂרָאֵל יְהוָה אֱלֹהֵינוּ יְהוָה אֶחָד׃"
SAMPLE_CITATION = "דְּבָרִים ו:ד"

CITATION_HEIGHT_RATIO = 0.18
CITATION_WIDTH_RATIO = 0.030
PASUK_HEIGHT_RATIO = 0.28
PASUK_WIDTH_RATIO = 0.028
MAX_PASUK_PIXELS = 28
MAX_CITATION_PIXELS = 14


def create_pasuk_display(parent):
    """Citation on the right; verse centered underneath. No card."""
    pasuk_display = tk.Frame(parent, bg=ROOT_BG_COLOR)
    hebrew = hebrew_font_family(parent)

    citation = tk.Label(
        pasuk_display,
        text=SAMPLE_CITATION,
        bg=ROOT_BG_COLOR,
        fg=MUTED_TEXT_COLOR,
        font=(hebrew, 11),
        anchor="e",
        justify="right",
    )
    pasuk_label = tk.Label(
        pasuk_display,
        text=SAMPLE_PASUK,
        bg=ROOT_BG_COLOR,
        fg=NAVY_COLOR,
        font=(hebrew, 20),
        anchor="center",
        justify="center",
    )

    citation.pack(fill="x", padx=8)
    pasuk_label.pack(fill="both", expand=True, padx=16, pady=(2, 4))
    pasuk_display.citation = citation
    pasuk_display.pasuk_label = pasuk_label
    pasuk_display.bind(
        "<Configure>", lambda event: redraw_pasuk_display(pasuk_display))
    return pasuk_display


def redraw_pasuk_display(pasuk_display):
    width = pasuk_display.winfo_width()
    height = pasuk_display.winfo_height()
    if width < 2 or height < 2:
        return

    hebrew = hebrew_font_family(pasuk_display)
    citation_size = max(
        9,
        min(
            MAX_CITATION_PIXELS,
            abs(fit_font_size(
                width, height, CITATION_HEIGHT_RATIO, CITATION_WIDTH_RATIO)),
        ),
    )
    pasuk_size = max(
        14,
        min(
            MAX_PASUK_PIXELS,
            abs(fit_font_size(
                width, height, PASUK_HEIGHT_RATIO, PASUK_WIDTH_RATIO)),
        ),
    )

    # Shrink until the full verse fits in the panel.
    pasuk_font = tkfont.Font(family=hebrew, size=pasuk_size)
    usable = max(80, width - 32)
    while pasuk_size > 14 and pasuk_font.measure(SAMPLE_PASUK) > usable:
        pasuk_size -= 1
        pasuk_font = tkfont.Font(family=hebrew, size=pasuk_size)

    pasuk_display.citation.configure(font=(hebrew, citation_size))
    pasuk_display.pasuk_label.configure(
        font=(hebrew, pasuk_size),
        wraplength=usable,
    )
