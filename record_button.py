import tkinter as tk
from dataclasses import dataclass
from voice_recorder import start_recording, stop_recording, RecordingState

BUTTON_SIZE = 100
BUTTON_BG_COLOR = "#0b1f4e"
ICON_COLOR = "white"
OUTPUT_FILENAME = "student_recording.wav"

def create_record_button(parent):
    record_button = tk.Canvas(
        parent,
        width=BUTTON_SIZE,
        height=BUTTON_SIZE,
        bg=BUTTON_BG_COLOR,
        highlightthickness=0,
        cursor="hand2"
    )
    set_record_button_icon(record_button, is_recording=False)
    return record_button


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
    center = BUTTON_SIZE / 2
    half_side = BUTTON_SIZE * 0.18
    canvas.create_rectangle(
        center - half_side, center - half_side,
        center + half_side, center + half_side,
        fill=ICON_COLOR, outline=ICON_COLOR, tags="icon"
    )


def draw_microphone_icon(canvas):
    center_x = BUTTON_SIZE / 2
    head_width = BUTTON_SIZE * 0.22
    head_top = BUTTON_SIZE * 0.28
    head_bottom = BUTTON_SIZE * 0.52

    canvas.create_rectangle(
        center_x - head_width / 2, head_top,
        center_x + head_width / 2, head_bottom,
        fill=ICON_COLOR, outline=ICON_COLOR, tags="icon"
    )
    canvas.create_arc(
        center_x - head_width / 2, head_top - head_width / 2,
        center_x + head_width / 2, head_top + head_width / 2,
        start=0, extent=180, fill=ICON_COLOR, outline=ICON_COLOR, tags="icon"
    )
    canvas.create_arc(
        center_x - head_width / 2, head_bottom - head_width / 2,
        center_x + head_width / 2, head_bottom + head_width / 2,
        start=180, extent=180, fill=ICON_COLOR, outline=ICON_COLOR, tags="icon"
    )

    stand_top = head_bottom - head_width * 0.1
    stand_height = BUTTON_SIZE * 0.14
    stand_width = head_width * 1.5

    canvas.create_arc(
        center_x - stand_width / 2, stand_top,
        center_x + stand_width / 2, stand_top + stand_height * 2,
        start=180, extent=180, outline=ICON_COLOR, width=3, style="arc", tags="icon"
    )
    canvas.create_line(
        center_x, stand_top + stand_height,
        center_x, stand_top + stand_height + BUTTON_SIZE * 0.08,
        fill=ICON_COLOR, width=3, tags="icon"
    )
    canvas.create_line(
        center_x - BUTTON_SIZE * 0.08, stand_top + stand_height + BUTTON_SIZE * 0.08,
        center_x + BUTTON_SIZE * 0.08, stand_top + stand_height + BUTTON_SIZE * 0.08,
        fill=ICON_COLOR, width=3, tags="icon"
    )