import tkinter as tk
from theme import FEEDBACK_BG_COLOR, FEEDBACK_TEXT_COLOR, FONT_FAMILY
from drawing import fit_font_size
from layout import FEEDBACK_LABEL_PLACEMENT

FEEDBACK_TEXT = "Perfect! You've mastered the pasuk!"   # placeholder until automated
PADDING_X = 16
TEXT_HEIGHT_RATIO = 0.38
TEXT_WIDTH_RATIO = 0.05


def create_feedback_label(parent):
    """
    Creates the feedback label. It is created on the parent but NOT placed,
    so it starts invisible.
    """
    feedback_label = tk.Label(
        parent,
        text=FEEDBACK_TEXT,
        bg=FEEDBACK_BG_COLOR,
        fg=FEEDBACK_TEXT_COLOR,
        anchor="w",
        justify="left",
        padx=PADDING_X
    )
    feedback_label.bind(
        "<Configure>", lambda event: redraw_feedback_label(feedback_label))
    return feedback_label


def show_feedback_label(feedback_label):
    feedback_label.place(**FEEDBACK_LABEL_PLACEMENT)


def hide_feedback_label(feedback_label):
    feedback_label.place_forget()


def redraw_feedback_label(feedback_label):
    width = feedback_label.winfo_width()
    height = feedback_label.winfo_height()
    feedback_label.configure(
        font=(FONT_FAMILY,
              fit_font_size(width, height, TEXT_HEIGHT_RATIO, TEXT_WIDTH_RATIO)),
        wraplength=max(1, width - 2 * PADDING_X)
    )
