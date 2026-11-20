import tkinter as tk

from theme import (ROOT_BG_COLOR, WHITE_COLOR, ACCENT_BLUE, DISABLED_FILL,
                   NAVY_COLOR, FONT_FAMILY)
from drawing import (create_rounded_rectangle, resize_rounded_rectangle,
                     set_canvas_fills, fit_font_size, bind_clickable)
from layout import PLAY_BUTTON_HEIGHT_RATIO
from audio_player import play_wav

INITIAL_SIZE = 60
CORNER_RADIUS_RATIO = 0.20
ICON_COLOR = WHITE_COLOR
LABEL_HEIGHT_RATIO = 0.35


def create_play_button(parent, label_text):
    """
    Creates a labeled play control: blue square with a clear Teacher/You
    caption underneath so the two play buttons are not identical mystery boxes.
    """
    frame = tk.Frame(parent, bg=ROOT_BG_COLOR)
    play_button = tk.Canvas(
        frame,
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

    caption = tk.Label(
        frame,
        text=label_text,
        bg=ROOT_BG_COLOR,
        fg=NAVY_COLOR,
        font=(FONT_FAMILY, 11, "bold")
    )
    play_button.pack()
    caption.pack(pady=(4, 0))
    frame.play_button = play_button
    frame.caption = caption
    play_button.caption = caption
    play_button.frame = frame
    return frame


def resize_play_button(play_frame, window_height):
    side = int(window_height * PLAY_BUTTON_HEIGHT_RATIO)
    play_frame.play_button.configure(width=side, height=side)
    label_size = fit_font_size(side * 2, side, LABEL_HEIGHT_RATIO, 0.22)
    play_frame.caption.configure(font=(FONT_FAMILY, abs(label_size), "bold"))


def redraw_play_button(play_button):
    width = play_button.winfo_width()
    height = play_button.winfo_height()
    fill = ACCENT_BLUE if play_button.enabled else DISABLED_FILL
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


def clear_play_button(play_button):
    """Forgets the linked file and disables the button."""
    play_button.audio_path = None
    set_play_button_enabled(play_button, False)


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


def bind_play_button(play_frame, command):
    """Wires click/hover on the square inside a labeled play control."""
    bind_clickable(play_frame.play_button, command, ACCENT_BLUE)


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
