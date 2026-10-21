# main.py
import tkinter as tk

from theme import ROOT_BG_COLOR
from layout import (LOGO_PLACEMENT, UPLOAD_BUTTON_PLACEMENT,
                    PASUK_DISPLAY_PLACEMENT, RECORD_BUTTON_PLACEMENT)
from logo import create_logo
from upload_button import create_upload_button, handle_upload_button_click
from pasuk_display import create_pasuk_display
from record_button import (create_record_button, handle_record_button_click,
                           resize_record_button, redraw_record_button)
from continue_button import (create_continue_button, handle_continue_button_click,
                             hide_continue_button)
from feedback_label import create_feedback_label, hide_feedback_label
from voice_recorder import RecordingState

ROOT_TITLE = "Learn To Lein App"
ROOT_GEOMETRY = "900x600"
ROOT_MIN_WIDTH = 640
ROOT_MIN_HEIGHT = 420

root = tk.Tk()
root.title(ROOT_TITLE)
root.geometry(ROOT_GEOMETRY)
root.minsize(ROOT_MIN_WIDTH, ROOT_MIN_HEIGHT)
root.configure(bg=ROOT_BG_COLOR)

# The one persistent copy of recording state
root.recording_state = RecordingState()

# --- Create components ---
logo = create_logo(root)
upload_button = create_upload_button(root)
pasuk_display = create_pasuk_display(root)
record_button = create_record_button(root)
continue_button = create_continue_button(root)
feedback_label = create_feedback_label(root)

# --- Place the visible components ---
logo.place(**LOGO_PLACEMENT)
upload_button.place(**UPLOAD_BUTTON_PLACEMENT)
pasuk_display.place(**PASUK_DISPLAY_PLACEMENT)
record_button.place(**RECORD_BUTTON_PLACEMENT)

# --- Event handlers ---
def on_root_resize(event):
    # <Configure> on root also fires for every child widget, so only react
    # when the event is actually about the root window.
    if event.widget is root:
        resize_record_button(record_button, event.height)

def on_record_button_resize(event):
    redraw_record_button(record_button, root.recording_state.is_recording)

def on_record_click(event):
    root.recording_state = handle_record_button_click(record_button, root.recording_state)

def on_upload_click(event):
    handle_upload_button_click(upload_button)


def on_continue_click(event):
    handle_continue_button_click(continue_button)

root.bind("<Configure>", on_root_resize)
record_button.bind("<Configure>", on_record_button_resize)
record_button.bind("<Button-1>", on_record_click)
upload_button.bind("<Button-1>", on_upload_click)
continue_button.bind("<Button-1>", on_continue_click)

root.mainloop()