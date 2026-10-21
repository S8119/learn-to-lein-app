import tkinter as tk
from tkinter import font as tkfont
from theme import (ROOT_BG_COLOR, LIGHT_GRAY_COLOR, GRAY_BORDER_COLOR,
                   DARK_TEXT_COLOR, FONT_FAMILY)
from drawing import create_rounded_rectangle, resize_rounded_rectangle, fit_font_size

UPLOAD_WORD = "Upload"
REST_OF_TITLE = " New File"
DEFAULT_FILENAME = "filename"

CORNER_RADIUS_RATIO = 0.18
MAIN_HEIGHT_RATIO = 0.30
MAIN_WIDTH_RATIO = 0.085
SUB_HEIGHT_RATIO = 0.18
SUB_WIDTH_RATIO = 0.055
MAIN_TEXT_Y_RATIO = 0.38
SUB_TEXT_Y_RATIO = 0.70


def create_upload_button(parent):
    """
    Creates the gray upload button: "Upload" underlined, " New File" after it,
    and a small "Current file: ..." line underneath.
    """
    upload_button = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0,
                              cursor="hand2")
    create_rounded_rectangle(upload_button, 0, 0, 1, 1, 1,
                             fill=LIGHT_GRAY_COLOR, outline=GRAY_BORDER_COLOR,
                             width=1, tags="background")
    upload_button.create_text(0, 0, text=UPLOAD_WORD, anchor="w",
                              fill=DARK_TEXT_COLOR, tags="upload_word")
    upload_button.create_text(0, 0, text=REST_OF_TITLE, anchor="w",
                              fill=DARK_TEXT_COLOR, tags="rest_of_title")
    upload_button.create_text(0, 0, text=f"Current file: {DEFAULT_FILENAME}",
                              fill=DARK_TEXT_COLOR, tags="filename_text")
    upload_button.bind("<Configure>", lambda event: redraw_upload_button(upload_button))
    return upload_button


def handle_upload_button_click(upload_button):
    """
    Called when the upload button is clicked.
    Empty for now: the logic for choosing and loading the teacher's
    recording will go here.
    """
    pass


def set_upload_button_filename(upload_button, filename):
    """Updates the 'Current file: ...' line. Call this once a file is chosen."""
    upload_button.itemconfigure("filename_text", text=f"Current file: {filename}")


def redraw_upload_button(upload_button):
    """
    Repositions and rescales the button's contents to fit its current size.
    "Upload" is underlined and " New File" is not, so they are two text
    items placed side by side, centered as a pair.
    """
    width = upload_button.winfo_width()
    height = upload_button.winfo_height()
    resize_rounded_rectangle(upload_button, "background", 1, 1, width - 1, height - 1,
                             height * CORNER_RADIUS_RATIO)

    main_size = fit_font_size(width, height, MAIN_HEIGHT_RATIO, MAIN_WIDTH_RATIO)
    sub_size = fit_font_size(width, height, SUB_HEIGHT_RATIO, SUB_WIDTH_RATIO)

    # Temporary fonts, used only to measure text widths.
    underlined_font = tkfont.Font(family=FONT_FAMILY, size=main_size, underline=True)
    normal_font = tkfont.Font(family=FONT_FAMILY, size=main_size)
    upload_word_width = underlined_font.measure(UPLOAD_WORD)
    rest_width = normal_font.measure(REST_OF_TITLE)
    start_x = (width - (upload_word_width + rest_width)) / 2
    main_y = height * MAIN_TEXT_Y_RATIO

    upload_button.coords("upload_word", start_x, main_y)
    upload_button.itemconfigure("upload_word",
                                font=(FONT_FAMILY, main_size, "underline"))
    upload_button.coords("rest_of_title", start_x + upload_word_width, main_y)
    upload_button.itemconfigure("rest_of_title", font=(FONT_FAMILY, main_size))
    upload_button.coords("filename_text", width / 2, height * SUB_TEXT_Y_RATIO)
    upload_button.itemconfigure("filename_text", font=(FONT_FAMILY, sub_size))