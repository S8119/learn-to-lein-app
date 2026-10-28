import sys
from tkinter import font as tkfont

ROOT_BG_COLOR = "#F7F4EC"
NAVY_COLOR = "#1B365D"
GOLD_COLOR = "#C4A35A"
WHITE_COLOR = "#FFFFFF"
CARD_BORDER_COLOR = "#E2D9C8"
MUTED_TEXT_COLOR = "#5C6570"
DARK_TEXT_COLOR = "#1A1A1A"
RECORDING_COLOR = "#C0392B"
SUCCESS_COLOR = "#2F6F4E"
FEEDBACK_BG_COLOR = "#E7F2EA"
FEEDBACK_TEXT_COLOR = "#2F6F4E"

HOVER_DARKEN = 0.92
PRESS_DARKEN = 0.84

# Use each operating system's native UI font so the app looks at home.
if sys.platform == "win32":
    FONT_FAMILY = "Segoe UI"
elif sys.platform == "darwin":
    FONT_FAMILY = "Helvetica Neue"
else:
    FONT_FAMILY = "DejaVu Sans"

# Prefer a face that places nikkud well; fall back if it is not installed.
HEBREW_FONT_CANDIDATES = (
    "David",
    "Gisha",
    "Narkisim",
    "Times New Roman",
    FONT_FAMILY
)


def darken_hex(color, factor=HOVER_DARKEN):
    """Returns a darker hex color. factor=1.0 is unchanged; 0.0 is black."""
    color = color.lstrip("#")
    red = int(int(color[0:2], 16) * factor)
    green = int(int(color[2:4], 16) * factor)
    blue = int(int(color[4:6], 16) * factor)
    return f"#{red:02x}{green:02x}{blue:02x}"


def hebrew_font_family(root=None):
    available = set(tkfont.families(root))
    for name in HEBREW_FONT_CANDIDATES:
        if name in available:
            return name
    return FONT_FAMILY
