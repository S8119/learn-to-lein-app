import ctypes
import sys
import tkinter as tk

from pathlib import Path

from theme import ROOT_BG_COLOR, NAVY_COLOR, WHITE_COLOR, SUCCESS_COLOR
from layout import (LOGO_PLACEMENT, UPLOAD_BUTTON_PLACEMENT,
                    PASUK_DISPLAY_PLACEMENT, RECORD_BUTTON_PLACEMENT,
                    TEACHER_PLAY_BUTTON_PLACEMENT, STUDENT_PLAY_BUTTON_PLACEMENT)
from drawing import bind_clickable
from logo import create_logo
from upload_button import create_upload_button, handle_upload_button_click
from pasuk_display import create_pasuk_display
from record_button import (create_record_button, handle_record_button_click,
                           resize_record_button, redraw_record_button,
                           OUTPUT_FILENAME, delete_student_recording)
from audio_uploader import delete_teacher_recordings
from timer_label import create_timer_label, start_timer_label, stop_timer_label
from play_button import (create_play_button, resize_play_button,
                         redraw_play_button, set_play_button_enabled,
                         handle_play_button_click, disable_play_buttons,
                         restore_play_buttons)
from audio_player import stop_playback
from trop_display import (create_trop_display, hide_trop_display,
                          update_trop_display)
from voice_recorder import RecordingState

ROOT_TITLE = "Learn to Lein"
ROOT_GEOMETRY = "900x600"
ROOT_MIN_WIDTH = 640
ROOT_MIN_HEIGHT = 420


def enable_windows_dpi_awareness():
    """
    Stop the app looking blurry on Windows.

    On a scaled display (125%, 150%, …), Windows otherwise draws the Tk
    window at 100% and stretches it, which makes text and controls fuzzy.
    This tells Windows to draw at the real pixel size instead. Linux and
    macOS skip it; they do not have that stretch-to-scale behavior.
    """
    if sys.platform == "win32":
        try:
            # 2 = process per-monitor DPI aware
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except (AttributeError, OSError):
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass


class App(tk.Tk):
    def __init__(self):
        enable_windows_dpi_awareness()
        super().__init__()
        self.title(ROOT_TITLE)
        self.geometry(ROOT_GEOMETRY)
        self.minsize(ROOT_MIN_WIDTH, ROOT_MIN_HEIGHT)
        self.configure(bg=ROOT_BG_COLOR)

        self.recording_state = RecordingState()
        delete_student_recording()
        delete_teacher_recordings()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.logo = create_logo(self)
        self.upload_button = create_upload_button(self)
        self.pasuk_display = create_pasuk_display(self)
        self.record_button = create_record_button(self)
        self.teacher_play_button = create_play_button(self)
        self.student_play_button = create_play_button(self)
        self.timer_label = create_timer_label(self)
        self.trop_display = create_trop_display(self)

        self.logo.place(**LOGO_PLACEMENT)
        self.upload_button.place(**UPLOAD_BUTTON_PLACEMENT)
        self.pasuk_display.place(**PASUK_DISPLAY_PLACEMENT)
        self.teacher_play_button.place(**TEACHER_PLAY_BUTTON_PLACEMENT)
        self.record_button.place(**RECORD_BUTTON_PLACEMENT)
        self.student_play_button.place(**STUDENT_PLAY_BUTTON_PLACEMENT)

        self.bind("<Configure>", self._on_resize)
        self.record_button.bind("<Configure>", self._on_record_button_resize)
        self.teacher_play_button.bind(
            "<Configure>", lambda event: redraw_play_button(self.teacher_play_button))
        self.student_play_button.bind(
            "<Configure>", lambda event: redraw_play_button(self.student_play_button))
        bind_clickable(self.record_button, self._on_record_click, NAVY_COLOR)
        bind_clickable(self.upload_button, self._on_upload_click, WHITE_COLOR)
        bind_clickable(self.teacher_play_button, self._on_teacher_play_click, SUCCESS_COLOR)
        bind_clickable(self.student_play_button, self._on_student_play_click, SUCCESS_COLOR)
        disable_play_buttons(self.teacher_play_button, self.student_play_button)

    def _on_resize(self, event):
        # <Configure> on the window also fires for every child widget, so
        # only react when the event is actually about this window.
        if event.widget is self:
            resize_record_button(self.record_button, event.height)
            resize_play_button(self.teacher_play_button, event.height)
            resize_play_button(self.student_play_button, event.height)

    def _on_record_button_resize(self, event):
        redraw_record_button(self.record_button, self.recording_state.is_recording)

    def _on_record_click(self, event):
        stop_playback()
        self.recording_state = handle_record_button_click(
            self.record_button, self.recording_state)
        if self.recording_state.is_recording:
            start_timer_label(self.timer_label)
            disable_play_buttons(
                self.teacher_play_button, self.student_play_button)
            hide_trop_display(self.trop_display)
        else:
            stop_timer_label(self.timer_label)
            student_path = Path(OUTPUT_FILENAME)
            if student_path.exists():
                set_play_button_enabled(
                    self.student_play_button, True, student_path)
                update_trop_display(
                    self.trop_display,
                    self.teacher_play_button.audio_path,
                    student_path)
            restore_play_buttons(
                self.teacher_play_button, self.student_play_button)

    def _on_upload_click(self, event):
        dest_path = handle_upload_button_click(self.upload_button)
        if dest_path is not None:
            set_play_button_enabled(
                self.teacher_play_button,
                not self.recording_state.is_recording,
                dest_path)
            update_trop_display(
                self.trop_display,
                dest_path,
                self.student_play_button.audio_path)

    def _on_teacher_play_click(self, event):
        handle_play_button_click(self.teacher_play_button)

    def _on_student_play_click(self, event):
        handle_play_button_click(self.student_play_button)

    def _on_close(self):
        stop_playback()
        if self.recording_state.stream is not None:
            self.recording_state.stream.stop()
            self.recording_state.stream.close()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
