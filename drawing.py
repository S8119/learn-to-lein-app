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
        x1, y1 + radius, x1, y1
    ]


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **options):
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


def set_canvas_fills(canvas, fill, tag="background"):
    """Stores idle/hover/press colors on the canvas and paints the idle color."""
    from theme import darken_hex, HOVER_DARKEN, PRESS_DARKEN

    canvas.base_fill = fill
    canvas.hover_fill = darken_hex(fill, HOVER_DARKEN)
    canvas.press_fill = darken_hex(fill, PRESS_DARKEN)
    if getattr(canvas, "_pressed", False):
        canvas.itemconfigure(tag, fill=canvas.press_fill)
    else:
        canvas.itemconfigure(tag, fill=fill)


def bind_clickable(canvas, command, fill, tag="background"):
    """
    Makes a canvas behave like a button: hover, press, and click on release.
    command(event) is called if the mouse is still over the canvas on release.
    """
    canvas.configure(cursor="hand2")
    canvas._pressed = False
    set_canvas_fills(canvas, fill, tag)

    def on_enter(_event):
        if not canvas._pressed:
            canvas.itemconfigure(tag, fill=canvas.hover_fill)

    def on_leave(_event):
        canvas._pressed = False
        canvas.itemconfigure(tag, fill=canvas.base_fill)

    def on_press(_event):
        canvas._pressed = True
        canvas.itemconfigure(tag, fill=canvas.press_fill)

    def on_release(event):
        was_pressed = canvas._pressed
        canvas._pressed = False
        canvas.itemconfigure(tag, fill=canvas.base_fill)
        if not was_pressed or command is None:
            return
        if 0 <= event.x <= canvas.winfo_width() and 0 <= event.y <= canvas.winfo_height():
            command(event)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)
