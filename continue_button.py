import tkinter as tk
from theme import ROOT_BG_COLOR, GREEN_COLOR, WHITE_COLOR, FONT_FAMILY
from drawing import create_rounded_rectangle, resize_rounded_rectangle, fit_font_size
from layout import CONTINUE_BUTTON_PLACEMENT

BUTTON_TEXT = "Next Pasuk"
CORNER_RADIUS_RATIO = 0.25
TEXT_HEIGHT_RATIO = 0.34
TEXT_WIDTH_RATIO = 0.10


def create_continue_button(parent):
    """
    Creates the continue button (green, "Next Pasuk"). It is created on the
    parent but NOT placed, so it starts invisible. The blue "Continue Anyway"
    version will be added later.
    """
    continue_button = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0,
                                cursor="hand2")
    create_rounded_rectangle(continue_button, 0, 0, 1, 1, 1,
                             fill=GREEN_COLOR, outline="", tags="background")
    continue_button.create_text(0, 0, text=BUTTON_TEXT, fill=WHITE_COLOR, tags="label")
    continue_button.bind("<Configure>", lambda event: redraw_continue_button(continue_button))
    return continue_button


def handle_continue_button_click(continue_button):
    """
    Called when the continue button is clicked.
    Empty for now: the logic for moving on to the next pasuk
    will go here.
    """
    pass


def show_continue_button(continue_button):
    continue_button.place(**CONTINUE_BUTTON_PLACEMENT)


def hide_continue_button(continue_button):
    continue_button.place_forget()


def redraw_continue_button(continue_button):
    width = continue_button.winfo_width()
    height = continue_button.winfo_height()
    resize_rounded_rectangle(continue_button, "background", 0, 0, width, height,
                             height * CORNER_RADIUS_RATIO)
    continue_button.coords("label", width / 2, height / 2)
    continue_button.itemconfigure(
        "label",
        font=(FONT_FAMILY,
              fit_font_size(width, height, TEXT_HEIGHT_RATIO, TEXT_WIDTH_RATIO),
              "bold")
    )