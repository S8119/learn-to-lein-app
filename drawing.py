# Small shared helpers for drawing on canvases.

MIN_FONT_PIXELS = 8

def rounded_rectangle_points(x1, y1, x2, y2, radius):
    """Returns the polygon points that, drawn with smooth=True, make a rounded rectangle."""
    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)
    return [
        x1 + radius, y1, x1 + radius, y1,
        x2 - radius, y1, x2 - radius, y1,
        x2, y1, x2, y1 + radius,
        x2, y1 + radius, x2, y2 - radius,
        x2, y2 - radius, x2, y2,
        x2 - radius, y2, x2 - radius, y2,
        x1 + radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius,
        x1, y2 - radius, x1, y1 + radius,
        x1, y1 + radius, x1, y1,
    ]


def create_rounded_rectangle(
        canvas, x1, y1, x2, y2, radius, **options):
    """Draws a rounded rectangle on the canvas and returns its item id."""
    return canvas.create_polygon(
        rounded_rectangle_points(x1, y1, x2, y2, radius),
        smooth=True, **options
    )


def resize_rounded_rectangle(canvas, item, x1, y1, x2, y2, radius):
    """Moves and resizes an existing rounded rectangle (item is an id or a tag)."""
    canvas.coords(item, *rounded_rectangle_points(x1, y1, x2, y2, radius))


def fit_font_size(width, height, height_ratio, width_ratio):
    """
    Returns a font size that scales with the widget. The size is the smaller
    of (height * height_ratio) and (width * width_ratio), so text never
    overflows in either direction. Negative means "pixels" to tkinter.
    """
    return -max(MIN_FONT_PIXELS, int(min(height * height_ratio, width * width_ratio)))