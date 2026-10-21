import tkinter as tk

from theme import ROOT_BG_COLOR
from layout import (LOGO_PLACEMENT, UPLOAD_BUTTON_PLACEMENT,
                    PASUK_DISPLAY_PLACEMENT, RECORD_BUTTON_PLACEMENT)
from logo import create_logo
from upload_button import create_upload_button, handle_upload_button_click
from pasuk_display import create_pasuk_display
from record_button import (create_record_button, handle_record_button_click,
                           resize_record_button, redraw_record_button)
from continue_button import create_continue_button, handle_continue_button_click
from feedback_label import create_feedback_label
from voice_recorder import RecordingState

ROOT_TITLE = "Learn To Lein App"
ROOT_GEOMETRY = "900x600"
ROOT_MIN_WIDTH = 640
ROOT_MIN_HEIGHT = 420


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(ROOT_TITLE)
        self.geometry(ROOT_GEOMETRY)
        self.minsize(ROOT_MIN_WIDTH, ROOT_MIN_HEIGHT)
        self.configure(bg=ROOT_BG_COLOR)

        self.recording_state = RecordingState()

        self.logo = create_logo(self)
        self.upload_button = create_upload_button(self)
        self.pasuk_display = create_pasuk_display(self)
        self.record_button = create_record_button(self)
        self.continue_button = create_continue_button(self)
        self.feedback_label = create_feedback_label(self)

        self.logo.place(**LOGO_PLACEMENT)
        self.upload_button.place(**UPLOAD_BUTTON_PLACEMENT)
        self.pasuk_display.place(**PASUK_DISPLAY_PLACEMENT)
        self.record_button.place(**RECORD_BUTTON_PLACEMENT)

        self.bind("<Configure>", self._on_resize)
        self.record_button.bind("<Configure>", self._on_record_button_resize)
        self.record_button.bind("<Button-1>", self._on_record_click)
        self.upload_button.bind("<Button-1>", self._on_upload_click)
        self.continue_button.bind("<Button-1>", self._on_continue_click)

    def _on_resize(self, event):
        # <Configure> on the window also fires for every child widget, so
        # only react when the event is actually about this window.
        if event.widget is self:
            resize_record_button(self.record_button, event.height)

    def _on_record_button_resize(self, event):
        redraw_record_button(self.record_button, self.recording_state.is_recording)

    def _on_record_click(self, event):
        self.recording_state = handle_record_button_click(
            self.record_button, self.recording_state)

    def _on_upload_click(self, event):
        handle_upload_button_click(self.upload_button)

    def _on_continue_click(self, event):
        handle_continue_button_click(self.continue_button)


if __name__ == "__main__":
    App().mainloop()
