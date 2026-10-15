# main.py
import tkinter as tk
from record_button import create_record_button, handle_record_button_click
from voice_recorder import RecordingState

ROOT_TITLE = "Learn To Lein App"
ROOT_GEOMETRY = "200x200"
ROOT_BG_COLOR = "#a9c9ea"

root = tk.Tk()
root.title(ROOT_TITLE)
root.geometry(ROOT_GEOMETRY)
root.configure(bg=ROOT_BG_COLOR)

# The one persistent copy of recording state
root.recording_state = RecordingState()

record_button = create_record_button(root)
record_button.pack(pady=50)


def on_click(event):
    root.recording_state = handle_record_button_click(record_button, root.recording_state)


record_button.bind("<Button-1>", on_click)

root.mainloop()