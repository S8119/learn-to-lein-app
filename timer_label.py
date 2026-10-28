import time
import tkinter as tk

from theme import ROOT_BG_COLOR, RECORDING_COLOR, FONT_FAMILY
from layout import TIMER_LABEL_PLACEMENT

INITIAL_TEXT = "0:00"
TICK_MS = 250


def create_timer_label(parent):
    """
    Creates the recording timer. It is created on the parent but NOT placed,
    so it starts invisible.
    """
    timer_label = tk.Label(
        parent,
        text=INITIAL_TEXT,
        bg=ROOT_BG_COLOR,
        fg=RECORDING_COLOR,
        font=(FONT_FAMILY, 14, "bold")
    )
    timer_label.job = None
    timer_label.started_at = None
    return timer_label


def start_timer_label(timer_label):
    stop_timer_label(timer_label)
    timer_label.started_at = time.monotonic()
    timer_label.configure(text=INITIAL_TEXT)
    timer_label.place(**TIMER_LABEL_PLACEMENT)
    _tick_timer_label(timer_label)


def stop_timer_label(timer_label):
    if timer_label.job is not None:
        timer_label.after_cancel(timer_label.job)
        timer_label.job = None
    timer_label.started_at = None
    timer_label.configure(text=INITIAL_TEXT)
    timer_label.place_forget()


def _tick_timer_label(timer_label):
    if timer_label.started_at is None:
        return
    elapsed = int(time.monotonic() - timer_label.started_at)
    minutes, seconds = divmod(elapsed, 60)
    timer_label.configure(text=f"{minutes}:{seconds:02d}")
    timer_label.job = timer_label.after(
        TICK_MS, lambda: _tick_timer_label(timer_label))
