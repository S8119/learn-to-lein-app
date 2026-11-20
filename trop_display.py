import tkinter as tk

from theme import (ROOT_BG_COLOR, PANEL_COLOR, NAVY_COLOR, GOLD_COLOR,
                   MUTED_TEXT_COLOR, FONT_FAMILY, RECORDING_COLOR,
                   SUCCESS_COLOR, GUIDE_LINE_COLOR, CARD_BORDER_COLOR)
from drawing import fit_font_size
from layout import TROP_DISPLAY_PLACEMENT
from audio_comparison import compare_trop, load_pitch_shape

PAD_RATIO = 0.06
TEACHER_LINE_COLOR = NAVY_COLOR
STUDENT_LINE_COLOR = GOLD_COLOR
LINE_WIDTH = 4
# The raw percent is for our math, not for the boy. He sees one of these.
RIGHT_SCORE = 100
CLOSE_SCORE = 90
RIGHT_MESSAGE = "You got it right"
CLOSE_MESSAGE = "You're close"
WRONG_MESSAGE = "That's not the trop"
EMPTY_HINT = "Upload a teacher recording, or record yourself, to see the trop"


def create_trop_display(parent):
    """
    Creates the trop stage. Always visible. Starts empty until a recording
    is uploaded or saved.
    """
    trop_display = tk.Canvas(
        parent, bg=ROOT_BG_COLOR, highlightthickness=0)
    trop_display.create_rectangle(
        0, 0, 1, 1,
        fill=PANEL_COLOR, outline=CARD_BORDER_COLOR, width=1, tags="background")
    trop_display.create_line(
        0, 0, 1, 0, fill=GUIDE_LINE_COLOR, width=1, tags="guide")
    trop_display.create_line(
        0, 0, 1, 1, fill=TEACHER_LINE_COLOR, width=LINE_WIDTH, tags="teacher_line")
    trop_display.create_line(
        0, 0, 1, 1, fill=STUDENT_LINE_COLOR, width=LINE_WIDTH, tags="student_line")
    trop_display.create_text(
        0, 0, text="Teacher", fill=NAVY_COLOR, anchor="w", tags="teacher_label")
    trop_display.create_text(
        0, 0, text="You", fill=GOLD_COLOR, anchor="w", tags="student_label")
    trop_display.create_text(
        0, 0, text="", fill=MUTED_TEXT_COLOR, anchor="e", tags="score_label")
    trop_display.create_text(
        0, 0, text=EMPTY_HINT, fill=MUTED_TEXT_COLOR, tags="hint")
    trop_display.teacher_shape = None
    trop_display.student_shape = None
    trop_display.score = None
    trop_display.off_tune = None
    trop_display.bind(
        "<Configure>", lambda event: redraw_trop_display(trop_display))
    return trop_display


def place_trop_display(trop_display):
    trop_display.place(**TROP_DISPLAY_PLACEMENT)
    redraw_trop_display(trop_display)


def clear_trop_display(trop_display):
    """Wipes teacher, student, and feedback off the stage."""
    trop_display.teacher_shape = None
    trop_display.student_shape = None
    trop_display.score = None
    trop_display.off_tune = None
    redraw_trop_display(trop_display)


def set_teacher_trop(trop_display, teacher_path):
    """
    Shows only the teacher line. Clears any student line/score first —
    used right after a teacher upload.
    """
    trop_display.student_shape = None
    trop_display.score = None
    trop_display.off_tune = None
    trop_display.teacher_shape = None
    if teacher_path is not None:
        trop_display.teacher_shape = load_pitch_shape(teacher_path)
    redraw_trop_display(trop_display)


def set_student_trop(trop_display, student_path):
    """Shows only the student line (no teacher file yet)."""
    trop_display.teacher_shape = None
    trop_display.score = None
    trop_display.off_tune = None
    trop_display.student_shape = None
    if student_path is not None:
        trop_display.student_shape = load_pitch_shape(student_path)
    redraw_trop_display(trop_display)


def update_trop_display(trop_display, teacher_path, student_path):
    """
    Updates the trop stage from whatever files exist right now.
    Teacher upload should call set_teacher_trop instead, so an old
    student take does not linger on the card.
    """
    if teacher_path is not None and student_path is not None:
        comparison = compare_trop(teacher_path, student_path)
        if comparison is None:
            trop_display.teacher_shape = load_pitch_shape(teacher_path)
            trop_display.student_shape = load_pitch_shape(student_path)
            trop_display.score = None
            trop_display.off_tune = None
        else:
            trop_display.teacher_shape = comparison["teacher_shape"]
            trop_display.student_shape = comparison["student_shape"]
            trop_display.score = comparison["score"]
            trop_display.off_tune = comparison.get("off_tune")
    elif teacher_path is not None:
        set_teacher_trop(trop_display, teacher_path)
        return
    elif student_path is not None:
        set_student_trop(trop_display, student_path)
        return
    else:
        clear_trop_display(trop_display)
        return
    redraw_trop_display(trop_display)


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


def _hide_line(trop_display, tag):
    trop_display.coords(tag, -10, -10, -10, -10)


def redraw_trop_display(trop_display):
    width = trop_display.winfo_width()
    height = trop_display.winfo_height()
    if width < 2 or height < 2:
        return

    trop_display.coords("background", 0, 0, width, height)

    pad = max(14, int(min(width, height) * PAD_RATIO))
    label_size = fit_font_size(width, height, 0.085, 0.028)
    hint_size = fit_font_size(width, height, 0.07, 0.022)

    trop_display.coords("teacher_label", pad, pad)
    trop_display.coords("student_label", pad + width * 0.16, pad)
    trop_display.coords("score_label", width - pad, pad)
    trop_display.itemconfigure(
        "teacher_label", font=(FONT_FAMILY, label_size, "bold"))
    trop_display.itemconfigure(
        "student_label", font=(FONT_FAMILY, label_size, "bold"))
    trop_display.itemconfigure("score_label", font=(FONT_FAMILY, label_size))

    has_teacher = trop_display.teacher_shape is not None
    has_student = trop_display.student_shape is not None
    trop_display.itemconfigure(
        "teacher_label", state="normal" if has_teacher else "hidden")
    trop_display.itemconfigure(
        "student_label", state="normal" if has_student else "hidden")

    if trop_display.score is not None:
        message, color = trop_feedback(trop_display.score)
        trop_display.itemconfigure("score_label", text=message, fill=color)
    else:
        trop_display.itemconfigure("score_label", text="")

    plot_top = pad * 2.6
    plot_left = pad
    plot_width = width - 2 * pad
    plot_height = height - plot_top - pad
    mid_y = plot_top + plot_height / 2
    trop_display.coords("guide", plot_left, mid_y, plot_left + plot_width, mid_y)

    trop_display.delete("miss")
    _hide_line(trop_display, "teacher_line")
    _hide_line(trop_display, "student_line")

    if not has_teacher and not has_student:
        trop_display.itemconfigure("hint", state="normal", font=(FONT_FAMILY, hint_size))
        trop_display.coords("hint", width / 2, height / 2)
        return

    trop_display.itemconfigure("hint", state="hidden")
    if plot_width < 2 or plot_height < 2:
        return

    shapes = []
    if has_teacher:
        shapes.append(trop_display.teacher_shape)
    if has_student:
        shapes.append(trop_display.student_shape)
    lowest = min(float(shape.min()) for shape in shapes)
    highest = max(float(shape.max()) for shape in shapes)
    lowest = min(lowest, -1.0)
    highest = max(highest, 1.0)

    if has_teacher:
        trop_display.coords(
            "teacher_line",
            *_line_points(
                trop_display.teacher_shape,
                plot_left, plot_top, plot_width, plot_height,
                lowest, highest))
    if has_student:
        student_points = _line_points(
            trop_display.student_shape,
            plot_left, plot_top, plot_width, plot_height,
            lowest, highest)
        trop_display.coords("student_line", *student_points)
        for start, end in _off_tune_runs(trop_display.off_tune):
            left = max(0, start - 1)
            right = min(len(trop_display.student_shape) - 1, end + 1)
            segment = student_points[2 * left:2 * right + 2]
            if len(segment) >= 4:
                trop_display.create_line(
                    *segment,
                    fill=RECORDING_COLOR,
                    width=LINE_WIDTH + 1,
                    tags="miss")
