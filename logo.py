import tkinter as tk
from theme import ROOT_BG_COLOR, NAVY_COLOR, FONT_FAMILY
from drawing import fit_font_size

WORDMARK = "Learn to Lein"
TEXT_HEIGHT_RATIO = 0.50
TEXT_WIDTH_RATIO = 0.11


def create_logo(parent):
    """Creates the wordmark in the header. Replace this with an image later."""
    logo = tk.Label(
        parent,
        text=WORDMARK,
        bg=ROOT_BG_COLOR,
        fg=NAVY_COLOR,
        anchor="w",
        font=(FONT_FAMILY, 20, "bold")
    )
    logo.bind("<Configure>", lambda event: redraw_logo(logo))
    return logo


def redraw_logo(logo):
    size = fit_font_size(
        logo.winfo_width(), logo.winfo_height(),
        TEXT_HEIGHT_RATIO, TEXT_WIDTH_RATIO)
    logo.configure(font=(FONT_FAMILY, size, "bold"))
