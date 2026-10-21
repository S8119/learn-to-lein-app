import tkinter as tk
from theme import ROOT_BG_COLOR, NAVY_COLOR, WHITE_COLOR
from drawing import create_rounded_rectangle, resize_rounded_rectangle
from layout import RECORD_BUTTON_HEIGHT_RATIO
from voice_recorder import start_recording, stop_recording, RecordingState

INITIAL_SIZE = 100
CORNER_RADIUS_RATIO = 0.22
ICON_COLOR = WHITE_COLOR
OUTPUT_FILENAME = "student_recording.wav"

# Microphone proportions, as fractions of the button's side length.
MIC_VERTICAL_SHIFT = 0.04       # nudges the whole icon so it is visually centered
MIC_CAPSULE_HALF_WIDTH = 0.13
MIC_CAPSULE_TOP = 0.16
MIC_CAPSULE_BOTTOM = 0.56
MIC_CRADLE_HALF_WIDTH = 0.22
MIC_CRADLE_TOP = 0.30
MIC_CRADLE_BOTTOM = 0.66
MIC_STEM_BOTTOM = 0.76
MIC_BASE_HALF_WIDTH = 0.12
MIC_LINE_WIDTH_RATIO = 0.045
STOP_SQUARE_RATIO = 0.32


def create_record_button(parent):
    """
    Creates the dark-blue rounded record/stop button. Its size and icon are
    filled in by redraw_record_button once the window gives it a size.
    """
    record_button = tk.Canvas(
        parent,
        width=INITIAL_SIZE,
        height=INITIAL_SIZE,
        bg=ROOT_BG_COLOR,
        highlightthickness=0,
        cursor="hand2"
    )
    create_rounded_rectangle(record_button, 0, 0, 1, 1, 1,
                             fill=NAVY_COLOR, outline="", tags="background")
    return record_button


def resize_record_button(record_button, window_height):
    """Makes the button a square whose side is a fraction of the window height."""
    side = int(window_height * RECORD_BUTTON_HEIGHT_RATIO)
    record_button.place_configure(width=side, height=side)


def redraw_record_button(record_button, is_recording):
    """Resizes the background to fit the button, then redraws the icon."""
    width = record_button.winfo_width()
    height = record_button.winfo_height()
    resize_rounded_rectangle(record_button, "background", 0, 0, width, height,
                             min(width, height) * CORNER_RADIUS_RATIO)
    set_record_button_icon(record_button, is_recording)


def handle_record_button_click(record_button, state):
    new_state = toggle_recording(state)
    set_record_button_icon(record_button, new_state.is_recording)
    return new_state


def toggle_recording(state):
    """
    Starts recording if currently idle; stops and saves if currently
    recording.
    """
    if not state.is_recording:
        stream, recording_frames, is_recording = start_recording()
        return RecordingState(is_recording=is_recording, stream=stream,
                              recording_frames=recording_frames)

    success = stop_recording(state.stream, state.recording_frames,
                             state.is_recording, OUTPUT_FILENAME)
    if success:
        print("Recording saved successfully.")
    else:
        print("Recording was not saved.")
    return RecordingState()


def set_record_button_icon(record_button, is_recording):
    record_button.delete("icon")
    if is_recording:
        draw_stop_icon(record_button)
    else:
        draw_microphone_icon(record_button)


def draw_stop_icon(canvas):
    """Draws a white rounded square in the center of the button."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    half_side = min(width, height) * STOP_SQUARE_RATIO / 2
    center_x = width / 2
    center_y = height / 2
    create_rounded_rectangle(
        canvas,
        center_x - half_side, center_y - half_side,
        center_x + half_side, center_y + half_side,
        half_side * 0.25,
        fill=ICON_COLOR, outline="", tags="icon"
    )


def draw_microphone_icon(canvas):
    """Draws a white microphone: a capsule, a cradle arc, a stem, and a base."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    size = min(width, height)
    center_x = width / 2
    origin_y = (height - size) / 2 + size * MIC_VERTICAL_SHIFT
    line_width = max(2, round(size * MIC_LINE_WIDTH_RATIO))

    capsule_half_width = size * MIC_CAPSULE_HALF_WIDTH
    capsule_top = origin_y + size * MIC_CAPSULE_TOP
    capsule_bottom = origin_y + size * MIC_CAPSULE_BOTTOM
    cradle_half_width = size * MIC_CRADLE_HALF_WIDTH
    cradle_top = origin_y + size * MIC_CRADLE_TOP
    cradle_bottom = origin_y + size * MIC_CRADLE_BOTTOM
    stem_bottom = origin_y + size * MIC_STEM_BOTTOM
    base_half_width = size * MIC_BASE_HALF_WIDTH

    # Capsule (the part you speak into)
    create_rounded_rectangle(
        canvas,
        center_x - capsule_half_width, capsule_top,
        center_x + capsule_half_width, capsule_bottom,
        capsule_half_width,
        fill=ICON_COLOR, outline="", tags="icon"
    )
    # Cradle: the lower half of an ellipse wrapped around the capsule
    canvas.create_arc(
        center_x - cradle_half_width, cradle_top,
        center_x + cradle_half_width, cradle_bottom,
        start=180, extent=180, style="arc",
        outline=ICON_COLOR, width=line_width, tags="icon"
    )
    # Stem and base
    canvas.create_line(
        center_x, cradle_bottom, center_x, stem_bottom,
        fill=ICON_COLOR, width=line_width, capstyle="round", tags="icon"
    )
    canvas.create_line(
        center_x - base_half_width, stem_bottom,
        center_x + base_half_width, stem_bottom,
        fill=ICON_COLOR, width=line_width, capstyle="round", tags="icon"
    )