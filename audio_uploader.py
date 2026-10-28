from pathlib import Path
from tkinter import filedialog, messagebox

# Keep teacher files out of the project root so a file named
# student_recording.wav cannot overwrite the boy's recording.
TEACHER_DIR = Path(__file__).resolve().parent / "teacher"
WAV_EXTENSION = ".wav"


def upload_audio_file(parent):
    """
    Opens a file dialog so the user can choose the teacher's WAV recording.
    Copies it into TEACHER_DIR under its original name. Returns that name
    for display, or None if the user cancelled or the copy failed.
    """
    window = parent.winfo_toplevel()
    chosen = filedialog.askopenfilename(
        parent=window,
        title="Upload teacher recording",
        filetypes=[("WAV audio", "*.wav")]
    )
    if not chosen:
        return None

    source_path = Path(chosen)
    if source_path.suffix.lower() != WAV_EXTENSION:
        messagebox.showerror(
            "Unsupported file",
            "Please choose a .wav file.",
            parent=window
        )
        return None

    TEACHER_DIR.mkdir(exist_ok=True)
    dest_path = TEACHER_DIR / source_path.name
    if source_path.resolve() != dest_path.resolve():
        try:
            source_path.copy(dest_path)
        except OSError as error:
            messagebox.showerror(
                "Upload failed",
                f"Could not copy the file:\n{error}",
                parent=window
            )
            return None

    return source_path.name
