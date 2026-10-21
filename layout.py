# Where each component goes, as fractions of the window (0.0 to 1.0).
# These are passed straight to widget.place(**PLACEMENT).

MARGIN_X = 0.02
MARGIN_Y = 0.03

LOGO_PLACEMENT = dict(
    relx=MARGIN_X, rely=MARGIN_Y, relwidth=0.20, relheight=0.12, anchor="nw")

UPLOAD_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=MARGIN_Y, relwidth=0.22, relheight=0.12, anchor="ne")

PASUK_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.21, relwidth=1 - 2 * MARGIN_X, relheight=0.40, anchor="nw")

# The record button's width and height are set in pixels by main.py so it
# stays a perfect square. Only its position is given here.
RECORD_BUTTON_PLACEMENT = dict(relx=0.5, rely=0.66, anchor="n")
RECORD_BUTTON_HEIGHT_RATIO = 0.19   # side length as a fraction of window height

CONTINUE_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=1 - MARGIN_Y, relwidth=0.20, relheight=0.11, anchor="se")

FEEDBACK_LABEL_PLACEMENT = dict(
    relx=MARGIN_X, rely=1 - MARGIN_Y, relwidth=0.50, relheight=0.09, anchor="sw")