import sys

ROOT_BG_COLOR = "#a9c9ea"
NAVY_COLOR = "#0b1f4e"
WHITE_COLOR = "white"
GREEN_COLOR = "#00b050"
BLUE_COLOR = "#0070c0"
LIGHT_GRAY_COLOR = "#e4e7eb"
GRAY_BORDER_COLOR = "#8c96a3"
DARK_TEXT_COLOR = "#1f2933"
FEEDBACK_BG_COLOR = "#d9f2d9"
FEEDBACK_TEXT_COLOR = "#2e8b3d"

# Use each operating system's native UI font so the app looks at home.
if sys.platform == "win32":
    FONT_FAMILY = "Segoe UI"
elif sys.platform == "darwin":
    FONT_FAMILY = "Helvetica Neue"
else:
    FONT_FAMILY = "DejaVu Sans"