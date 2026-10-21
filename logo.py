import tkinter as tk
from theme import ROOT_BG_COLOR, WHITE_COLOR, GRAY_BORDER_COLOR, DARK_TEXT_COLOR, FONT_FAMILY
from drawing import create_rounded_rectangle, resize_rounded_rectangle, fit_font_size

LOGO_TEXT = "App's Logo Here"
CORNER_RADIUS_RATIO = 0.18      # corner radius as a fraction of height
TEXT_HEIGHT_RATIO = 0.32
TEXT_WIDTH_RATIO = 0.11


def create_logo(parent):
    """Creates the logo placeholder: a white rounded rectangle with text."""
    logo = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0)
    create_rounded_rectangle(logo, 0, 0, 1, 1, 1,
                             fill=WHITE_COLOR, outline=GRAY_BORDER_COLOR,
                             width=1, tags="background")
    logo.create_text(0, 0, text=LOGO_TEXT, fill=DARK_TEXT_COLOR, tags="label")
    logo.bind("<Configure>", lambda event: redraw_logo(logo))
    return logo


def redraw_logo(logo):
    """Repositions and rescales the logo's contents to fit its current size."""
    width = logo.winfo_width()
    height = logo.winfo_height()
    resize_rounded_rectangle(logo, "background", 1, 1, width - 1, height - 1,
                             height * CORNER_RADIUS_RATIO)
    logo.coords("label", width / 2, height / 2)
    logo.itemconfigure(
        "label",
        font=(FONT_FAMILY, fit_font_size(width, height, TEXT_HEIGHT_RATIO, TEXT_WIDTH_RATIO))
    )