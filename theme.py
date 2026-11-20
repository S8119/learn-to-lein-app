import sys
from tkinter import font as tkfont

from font_loader import HEBREW_FAMILY_NAMES

# Light parchment with navy + gold — warm, not muddy brown.
ROOT_BG_COLOR = "#F7F2E7"
PANEL_COLOR = "#FFFCF7"
NAVY_COLOR = "#1B365D"
ACCENT_BLUE = "#2F6FAD"
GOLD_COLOR = "#C4A35A"
WHITE_COLOR = "#FFFFFF"
CARD_BORDER_COLOR = "#D9E0EA"
MUTED_TEXT_COLOR = "#5C6B7A"
DARK_TEXT_COLOR = "#1A2433"
RECORDING_COLOR = "#C0392B"
SUCCESS_COLOR = "#2F6F4E"
GUIDE_LINE_COLOR = "#D5DCE6"
# Cool slate for disabled controls — not brown.
DISABLED_FILL = "#8A97A8"

HOVER_DARKEN = 0.92
PRESS_DARKEN = 0.84

if sys.platform == "win32":
    FONT_FAMILY = "Candara"
elif sys.platform == "darwin":
    FONT_FAMILY = "Avenir Next"
else:
    FONT_FAMILY = "DejaVu Sans"

HEBREW_FONT_CANDIDATES = (
    *HEBREW_FAMILY_NAMES,
    "SBL Hebrew",
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
