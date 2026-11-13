import tkinter as tk

from theme import (ROOT_BG_COLOR, WHITE_COLOR, NAVY_COLOR, GOLD_COLOR,
                   MUTED_TEXT_COLOR, FONT_FAMILY, RECORDING_COLOR,
                   SUCCESS_COLOR)
from drawing import (create_rounded_rectangle, resize_rounded_rectangle,
                     fit_font_size)
from layout import TROP_DISPLAY_PLACEMENT
from audio_comparison import compare_trop

CORNER_RADIUS_RATIO = 0.08
PAD_RATIO = 0.10
TEACHER_LINE_COLOR = NAVY_COLOR
STUDENT_LINE_COLOR = GOLD_COLOR
# The raw percent is for our math, not for the boy. He sees one of these.
RIGHT_SCORE = 100
CLOSE_SCORE = 90
RIGHT_MESSAGE = "You got it right"
CLOSE_MESSAGE = "You're close"
WRONG_MESSAGE = "That's not the trop"


def create_trop_display(parent):
    """
    Creates the trop-shape card. It is created on the parent but NOT placed,
    so it starts invisible.
    """
    trop_display = tk.Canvas(parent, bg=ROOT_BG_COLOR, highlightthickness=0)
    create_rounded_rectangle(
        trop_display, 0, 0, 1, 1, 1,
        fill=WHITE_COLOR, outline="", tags="background")
    trop_display.create_line(0, 0, 1, 1, fill=TEACHER_LINE_COLOR, width=2, tags="teacher_line")
    trop_display.create_line(0, 0, 1, 1, fill=STUDENT_LINE_COLOR, width=2, tags="student_line")
    trop_display.create_text(0, 0, text="Teacher", fill=NAVY_COLOR, anchor="w", tags="teacher_label")
    trop_display.create_text(0, 0, text="You", fill=GOLD_COLOR, anchor="w", tags="student_label")
    trop_display.create_text(0, 0, text="", fill=MUTED_TEXT_COLOR, anchor="e", tags="score_label")
    trop_display.teacher_shape = None
    trop_display.student_shape = None
    trop_display.score = None
    trop_display.off_tune = None
    trop_display.bind(
        "<Configure>", lambda event: redraw_trop_display(trop_display))
    return trop_display


def show_trop_display(trop_display, comparison):
    trop_display.teacher_shape = comparison["teacher_shape"]
    trop_display.student_shape = comparison["student_shape"]
    trop_display.score = comparison["score"]
    trop_display.off_tune = comparison.get("off_tune")
    trop_display.place(**TROP_DISPLAY_PLACEMENT)
    redraw_trop_display(trop_display)


def hide_trop_display(trop_display):
    trop_display.place_forget()


def update_trop_display(trop_display, teacher_path, student_path):
    """Shows the trop card if both files can be compared; hides it otherwise."""
    comparison = None
    if teacher_path is not None and student_path is not None:
        comparison = compare_trop(teacher_path, student_path)
    if comparison is None:
        hide_trop_display(trop_display)
    else:
        show_trop_display(trop_display, comparison)


def _line_points(shape, left, top, width, height, lowest, highest):
    # Both lines must share this vertical scale. If each line used its
    # own min/max, a flatter take would be stretched to fill the card
    # and look like a different tune.
    span = max(highest - lowest, 1.0)
    points = []
    for index, value in enumerate(shape):
        x = left + (index / (len(shape) - 1)) * width
        y = top + (1 - (value - lowest) / span) * height
        points.extend((x, y))
    return points


def trop_feedback(score):
    """Turns the internal score into a short verdict, with no percent."""
    if score >= RIGHT_SCORE:
        message = RIGHT_MESSAGE
        color = SUCCESS_COLOR
    elif score >= CLOSE_SCORE:
        message = CLOSE_MESSAGE
        color = GOLD_COLOR
    else:
        message = WRONG_MESSAGE
        color = RECORDING_COLOR
    return message, color


def _off_tune_runs(off_tune):
    """Start/end index pairs for each stretch marked off-tune."""
    runs = []
    run_start = None
    if off_tune is not None:
        for index, is_off in enumerate(off_tune):
            if is_off:
                if run_start is None:
                    run_start = index
            else:
                if run_start is not None:
                    runs.append((run_start, index - 1))
                    run_start = None
        if run_start is not None:
            runs.append((run_start, len(off_tune) - 1))
    return runs


def redraw_trop_display(trop_display):
    width = trop_display.winfo_width()
    height = trop_display.winfo_height()
    if width >= 2 and height >= 2:
        resize_rounded_rectangle(
            trop_display, "background", 0, 0, width, height,
            height * CORNER_RADIUS_RATIO)

        pad = max(8, int(height * PAD_RATIO))
        label_size = fit_font_size(width, height, 0.22, 0.035)
        trop_display.coords("teacher_label", pad, pad)
        trop_display.coords("student_label", pad + width * 0.18, pad)
        trop_display.coords("score_label", width - pad, pad)
        trop_display.itemconfigure(
            "teacher_label", font=(FONT_FAMILY, label_size, "bold"))
        trop_display.itemconfigure(
            "student_label", font=(FONT_FAMILY, label_size, "bold"))
        trop_display.itemconfigure("score_label", font=(FONT_FAMILY, label_size))

        if trop_display.score is not None:
            message, color = trop_feedback(trop_display.score)
            trop_display.itemconfigure("score_label", text=message, fill=color)
        else:
            trop_display.itemconfigure("score_label", text="")

        plot_top = pad * 2.4
        plot_left = pad
        plot_width = width - 2 * pad
        plot_height = height - plot_top - pad
        has_shapes = (
            trop_display.teacher_shape is not None
            and trop_display.student_shape is not None
        )
        if has_shapes and plot_width >= 2 and plot_height >= 2:
            lowest = min(
                float(trop_display.teacher_shape.min()),
                float(trop_display.student_shape.min()),
                -1.0)
            highest = max(
                float(trop_display.teacher_shape.max()),
                float(trop_display.student_shape.max()),
                1.0)
            trop_display.coords(
                "teacher_line",
                *_line_points(
                    trop_display.teacher_shape,
                    plot_left, plot_top, plot_width, plot_height,
                    lowest, highest))
            trop_display.coords(
                "student_line",
                *_line_points(
                    trop_display.student_shape,
                    plot_left, plot_top, plot_width, plot_height,
                    lowest, highest))
            trop_display.delete("miss")
            student_points = _line_points(
                trop_display.student_shape,
                plot_left, plot_top, plot_width, plot_height,
                lowest, highest)
            for start, end in _off_tune_runs(trop_display.off_tune):
                # One extra neighbor so the red mark meets the gold line.
                left = max(0, start - 1)
                right = min(len(trop_display.student_shape) - 1, end + 1)
                segment = student_points[2 * left:2 * right + 2]
                if len(segment) >= 4:
                    trop_display.create_line(
                        *segment,
                        fill=RECORDING_COLOR,
                        width=3,
                        tags="miss")
