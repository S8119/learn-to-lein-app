import tkinter as tk

from theme import ROOT_BG_COLOR, WHITE_COLOR, SUCCESS_COLOR, MUTED_TEXT_COLOR
from drawing import (create_rounded_rectangle, resize_rounded_rectangle,
                     set_canvas_fills)
from layout import PLAY_BUTTON_HEIGHT_RATIO
from audio_player import play_wav

INITIAL_SIZE = 60
CORNER_RADIUS_RATIO = 0.22
ICON_COLOR = WHITE_COLOR
DISABLED_FILL = MUTED_TEXT_COLOR


def create_play_button(parent):
    """
    Creates a green play button. It starts disabled until a recording
    path is set with set_play_button_enabled.
    """
    play_button = tk.Canvas(
        parent,
        width=INITIAL_SIZE,
        height=INITIAL_SIZE,
        bg=ROOT_BG_COLOR,
        highlightthickness=0,
        cursor="arrow"
    )
    create_rounded_rectangle(
        play_button, 0, 0, 1, 1, 1,
        fill=DISABLED_FILL, outline="", tags="background")
    play_button.enabled = False
    play_button.audio_path = None
    set_canvas_fills(play_button, DISABLED_FILL)
    return play_button


def resize_play_button(play_button, window_height):
    side = int(window_height * PLAY_BUTTON_HEIGHT_RATIO)
    play_button.place_configure(width=side, height=side)


def redraw_play_button(play_button):
    width = play_button.winfo_width()
    height = play_button.winfo_height()
    fill = SUCCESS_COLOR if play_button.enabled else DISABLED_FILL
    resize_rounded_rectangle(
        play_button, "background", 0, 0, width, height,
        min(width, height) * CORNER_RADIUS_RATIO)
    set_canvas_fills(play_button, fill)
    draw_play_icon(play_button)


def set_play_button_enabled(play_button, enabled, audio_path=None):
    play_button.enabled = enabled
    if audio_path is not None:
        play_button.audio_path = audio_path
    play_button.configure(cursor="hand2" if enabled else "arrow")
    redraw_play_button(play_button)


def handle_play_button_click(play_button):
    if play_button.enabled and play_button.audio_path is not None:
        play_wav(play_button.audio_path)


def disable_play_buttons(*play_buttons):
    for play_button in play_buttons:
        set_play_button_enabled(play_button, False)


def restore_play_buttons(*play_buttons):
    for play_button in play_buttons:
        if play_button.audio_path is not None:
            set_play_button_enabled(play_button, True)


def draw_play_icon(canvas):
    canvas.delete("icon")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    size = min(width, height)
    center_x = width / 2
    center_y = height / 2
    left = center_x - size * 0.10
    right = center_x + size * 0.20
    top = center_y - size * 0.18
    bottom = center_y + size * 0.18
    canvas.create_polygon(
        left, top, right, center_y, left, bottom,
        fill=ICON_COLOR, outline="", tags="icon"
    )
