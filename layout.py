# Where each component goes, as fractions of the window (0.0 to 1.0).
# These are passed straight to widget.place(**PLACEMENT).

MARGIN_X = 0.04
MARGIN_Y = 0.028

LOGO_PLACEMENT = dict(
    relx=MARGIN_X, rely=MARGIN_Y, relwidth=0.40, relheight=0.06, anchor="nw")

UPLOAD_BUTTON_PLACEMENT = dict(
    relx=1 - MARGIN_X, rely=MARGIN_Y, relwidth=0.32, relheight=0.07, anchor="ne")

# Pasuk sits light above the trop stage — secondary, not a hero card.
PASUK_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.10, relwidth=1 - 2 * MARGIN_X, relheight=0.12, anchor="nw")

# Trop graph is the main stage.
TROP_DISPLAY_PLACEMENT = dict(
    relx=MARGIN_X, rely=0.23, relwidth=1 - 2 * MARGIN_X, relheight=0.42, anchor="nw")

# Bottom practice strip: teacher play, mic, student play.
TEACHER_PLAY_BUTTON_PLACEMENT = dict(relx=0.30, rely=0.76, anchor="n")
RECORD_BUTTON_PLACEMENT = dict(relx=0.5, rely=0.73, anchor="n")
STUDENT_PLAY_BUTTON_PLACEMENT = dict(relx=0.70, rely=0.76, anchor="n")

# Sizes are set in pixels by main.py so the buttons stay square.
RECORD_BUTTON_HEIGHT_RATIO = 0.13
PLAY_BUTTON_HEIGHT_RATIO = 0.075

TIMER_LABEL_PLACEMENT = dict(relx=0.5, rely=0.92, anchor="n")
