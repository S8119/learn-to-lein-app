# Where each component goes, as fractions of the window (0.0 to 1.0).
# These are passed straight to widget.place(**PLACEMENT).

MARGIN_X = 0.04
MARGIN_Y = 0.03

LOGO_PLACEMENT = dict(
    relx=MARGIN_X, rely=MARGIN_Y, relwidth=0.42, relheight=0.08, anchor="nw")

UPLOAD_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=MARGIN_Y, relwidth=0.28, relheight=0.08, anchor="ne")

PASUK_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.14, relwidth=1 - 2 * MARGIN_X, relheight=0.42, anchor="nw")

# Teacher play sits on the left of the pasuk, next to the Hebrew.
TEACHER_PLAY_BUTTON_PLACEMENT = dict(
    relx=MARGIN_X + 0.015, rely=0.33, anchor="w")

TROP_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.58, relwidth=1 - 2 * MARGIN_X, relheight=0.10, anchor="nw")

# The record button's width and height are set in pixels by main.py so it
# stays a perfect square. Only its position is given here.
RECORD_BUTTON_PLACEMENT = dict(relx=0.5, rely=0.68, anchor="n")
RECORD_BUTTON_HEIGHT_RATIO = 0.16   # side length as a fraction of window height

# Student play sits to the right of the microphone.
STUDENT_PLAY_BUTTON_PLACEMENT = dict(relx=0.68, rely=0.72, anchor="n")
PLAY_BUTTON_HEIGHT_RATIO = 0.09

TIMER_LABEL_PLACEMENT = dict(relx=0.5, rely=0.86, anchor="n")
