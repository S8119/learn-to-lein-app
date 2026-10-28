import tkinter as tk
from theme import (ROOT_BG_COLOR, WHITE_COLOR, GOLD_COLOR, NAVY_COLOR,
                   MUTED_TEXT_COLOR, hebrew_font_family)
from drawing import (create_rounded_rectangle, resize_rounded_rectangle,
                     fit_font_size)

# Stand-in for the one-pasuk prototype. Swap this when you pick a test pasuk.
SAMPLE_PASUK = "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ׃"
SAMPLE_CITATION = "בְּרֵאשִׁית א:א"

CORNER_RADIUS_RATIO = 0.04
CITATION_HEIGHT_RATIO = 0.08
CITATION_WIDTH_RATIO = 0.04
PASUK_HEIGHT_RATIO = 0.16
PASUK_WIDTH_RATIO = 0.055


def create_pasuk_display(parent):
    """
    Creates the pasuk card: a rounded panel with a citation and the Hebrew
    verse in a real Text widget (better wrapping and nikkud than canvas text).
    """
    pasuk_display = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0)
    create_rounded_rectangle(
        pasuk_display, 0, 0, 1, 1, 1,
        fill=WHITE_COLOR, outline=GOLD_COLOR, width=1, tags="background")

    citation = tk.Label(
        pasuk_display,
        text=SAMPLE_CITATION,
        bg=WHITE_COLOR,
        fg=MUTED_TEXT_COLOR,
        font=(hebrew_font_family(parent), 12),
        anchor="e"
    )
    pasuk_text = tk.Text(
        pasuk_display,
        wrap="word",
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        bg=WHITE_COLOR,
        fg=NAVY_COLOR,
        cursor="arrow",
        padx=12,
        pady=8
    )
    pasuk_text.insert("1.0", SAMPLE_PASUK)
    pasuk_text.tag_configure("pasuk", justify="center")
    pasuk_text.tag_add("pasuk", "1.0", "end")
    pasuk_text.configure(state="disabled")

    pasuk_display.create_window(0, 0, window=citation, anchor="ne", tags="citation")
    pasuk_display.create_window(0, 0, window=pasuk_text, anchor="n", tags="pasuk_text")
    pasuk_display.citation = citation
    pasuk_display.pasuk_text = pasuk_text
    pasuk_display.bind(
        "<Configure>", lambda event: redraw_pasuk_display(pasuk_display))
    return pasuk_display


def redraw_pasuk_display(pasuk_display):
    width = pasuk_display.winfo_width()
    height = pasuk_display.winfo_height()
    resize_rounded_rectangle(
        pasuk_display, "background", 2, 2, width - 2, height - 2,
        height * CORNER_RADIUS_RATIO)

    pad_x = max(20, int(width * 0.04))
    pad_y = max(16, int(height * 0.08))
    citation_space = max(22, int(height * 0.12))
    inner_width = max(1, width - 2 * pad_x)
    text_height = max(1, height - pad_y - citation_space - pad_y)

    pasuk_display.coords("citation", width - pad_x, pad_y)
    pasuk_display.coords("pasuk_text", width / 2, pad_y + citation_space)
    pasuk_display.itemconfigure(
        "pasuk_text", width=inner_width, height=text_height)

    citation_size = fit_font_size(
        width, height, CITATION_HEIGHT_RATIO, CITATION_WIDTH_RATIO)
    pasuk_size = fit_font_size(
        width, height, PASUK_HEIGHT_RATIO, PASUK_WIDTH_RATIO)
    pasuk_display.citation.configure(
        font=(hebrew_font_family(pasuk_display), citation_size))

    pasuk_text = pasuk_display.pasuk_text
    pasuk_text.configure(state="normal")
    pasuk_text.tag_configure(
        "pasuk",
        justify="center",
        font=(hebrew_font_family(pasuk_display), pasuk_size),
        foreground=NAVY_COLOR
    )
    pasuk_text.configure(state="disabled")
