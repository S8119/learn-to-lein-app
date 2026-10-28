import tkinter as tk
from theme import (ROOT_BG_COLOR, WHITE_COLOR, CARD_BORDER_COLOR,
                   NAVY_COLOR, MUTED_TEXT_COLOR, FONT_FAMILY)
from drawing import create_rounded_rectangle, resize_rounded_rectangle, fit_font_size
from audio_uploader import upload_audio_file

TITLE_TEXT = "Upload recording"
NO_FILE_TEXT = "No file chosen"

CORNER_RADIUS_RATIO = 0.22
MAIN_HEIGHT_RATIO = 0.34
MAIN_WIDTH_RATIO = 0.075
SUB_HEIGHT_RATIO = 0.22
SUB_WIDTH_RATIO = 0.055
MAIN_TEXT_Y_RATIO = 0.38
SUB_TEXT_Y_RATIO = 0.70


def create_upload_button(parent):
    """
    Creates the upload button: a short title and a line for the current
    teacher file (or "No file chosen" until one is picked).
    """
    upload_button = tk.Canvas(
        parent, bg=ROOT_BG_COLOR, highlightthickness=0, cursor="hand2")
    create_rounded_rectangle(
        upload_button, 0, 0, 1, 1, 1,
        fill=WHITE_COLOR, outline=CARD_BORDER_COLOR, width=1, tags="background")
    upload_button.create_text(
        0, 0, text=TITLE_TEXT, fill=NAVY_COLOR, tags="title_text")
    upload_button.create_text(
        0, 0, text=NO_FILE_TEXT, fill=MUTED_TEXT_COLOR, tags="filename_text")
    upload_button.bind(
        "<Configure>", lambda event: redraw_upload_button(upload_button))
    return upload_button


def handle_upload_button_click(upload_button):
    filename = upload_audio_file(upload_button)
    if filename is not None:
        set_upload_button_filename(upload_button, filename)


def set_upload_button_filename(upload_button, filename):
    """Updates the subtitle. Call this once a file is chosen."""
    upload_button.itemconfigure("filename_text", text=filename)


def redraw_upload_button(upload_button):
    width = upload_button.winfo_width()
    height = upload_button.winfo_height()
    resize_rounded_rectangle(
        upload_button, "background", 1, 1, width - 1, height - 1,
        height * CORNER_RADIUS_RATIO)

    main_size = fit_font_size(width, height, MAIN_HEIGHT_RATIO, MAIN_WIDTH_RATIO)
    sub_size = fit_font_size(width, height, SUB_HEIGHT_RATIO, SUB_WIDTH_RATIO)

    upload_button.coords("title_text", width / 2, height * MAIN_TEXT_Y_RATIO)
    upload_button.itemconfigure(
        "title_text", font=(FONT_FAMILY, main_size, "bold"))
    upload_button.coords("filename_text", width / 2, height * SUB_TEXT_Y_RATIO)
    upload_button.itemconfigure(
        "filename_text", font=(FONT_FAMILY, sub_size))
