import tkinter as tk
from theme import ROOT_BG_COLOR, WHITE_COLOR
from drawing import create_rounded_rectangle, resize_rounded_rectangle

CORNER_RADIUS_RATIO = 0.06


def create_pasuk_display(parent):
    """Creates the blank white rounded rectangle where the pasuk will be shown."""
    pasuk_display = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0)
    create_rounded_rectangle(pasuk_display, 0, 0, 1, 1, 1,
                             fill=WHITE_COLOR, outline="", tags="background")
    pasuk_display.bind("<Configure>", lambda event: redraw_pasuk_display(pasuk_display))
    return pasuk_display


def redraw_pasuk_display(pasuk_display):
    width = pasuk_display.winfo_width()
    height = pasuk_display.winfo_height()
    resize_rounded_rectangle(pasuk_display, "background", 0, 0, width, height,
                             height * CORNER_RADIUS_RATIO)