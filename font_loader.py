"""
Loads the bundled OFL Hebrew font for this process.

Bundled font (see license file in fonts/):
- Frank Ruhl Libre — SIL OFL (classic chumash-style letters)

We keep the license file next to the .ttf and do not rename
Reserved Font Names.
"""
import sys
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent / "fonts"
# Use the static Regular face. The variable .ttf smushes Hebrew in Tk.
FRANK_RUHL = FONTS_DIR / "FrankRuhlLibre-Regular.ttf"

HEBREW_FAMILY_NAMES = (
    "Frank Ruhl Libre",
)

_loaded = False


def load_bundled_hebrew_fonts():
    """
    Makes the bundled Hebrew font available to Tk for this run.
    On Windows we register the file with GDI for the current process only.
    """
    global _loaded
    loaded_any = _loaded
    if not _loaded and sys.platform == "win32":
        import ctypes
        add_font = ctypes.windll.gdi32.AddFontResourceExW
        # FR_PRIVATE = 0x10: only this process sees the font.
        FR_PRIVATE = 0x10
        if FRANK_RUHL.exists():
            result = add_font(str(FRANK_RUHL), FR_PRIVATE, 0)
            if result:
                loaded_any = True
        _loaded = True
    return loaded_any
