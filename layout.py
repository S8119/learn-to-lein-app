# Where each component goes, as fractions of the window (0.0 to 1.0).
# These are passed straight to widget.place(**PLACEMENT).

MARGIN_X = 0.04
MARGIN_Y = 0.03

LOGO_PLACEMENT = dict(
    relx=MARGIN_X, rely=MARGIN_Y, relwidth=0.42, relheight=0.08, anchor="nw")

UPLOAD_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=MARGIN_Y, relwidth=0.28, relheight=0.08, anchor="ne")

PASUK_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.14, relwidth=1 - 2 * MARGIN_X, relheight=0.50, anchor="nw")

# The record button's width and height are set in pixels by main.py so it
# stays a perfect square. Only its position is given here.
RECORD_BUTTON_PLACEMENT = dict(relx=0.5, rely=0.68, anchor="n")
RECORD_BUTTON_HEIGHT_RATIO = 0.16   # side length as a fraction of window height

TIMER_LABEL_PLACEMENT = dict(relx=0.5, rely=0.86, anchor="n")

CONTINUE_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=1 - MARGIN_Y, relwidth=0.20, relheight=0.09, anchor="se")

FEEDBACK_LABEL_PLACEMENT = dict(
    relx=MARGIN_X, rely=1 - MARGIN_Y, relwidth=0.50, relheight=0.09, anchor="sw")
