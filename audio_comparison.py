"""
Trop comparison: we do not turn speech into words. We measure how the
voice goes up and down (the tune) and compare those two shapes.

A few terms used below:
- Hz (hertz): how many times the vocal cords vibrate per second. A higher
  number is a higher note. Adult men are often ~80–180 Hz; boys and women
  are often higher.
- Semitone: one piano key. There are 12 semitones in an octave (a jump that
  sounds like the same note, higher). We convert Hz to semitones so “the
  same tune, sung lower” still looks like a match.
"""
from pathlib import Path

import librosa
import numpy

# How many dots we keep in the drawn trop line (left = start, right = end).
COMPARISON_POINTS = 120
# Ignore a clip that barely has any sung/spoken pitch.
MIN_VOICED_FRAMES = 8
SEMITONES_PER_OCTAVE = 12.0
# Average neighboring dots so leftover tracker jitter is not the score.
SMOOTH_WIDTH = 5
# How far one reader may drift in time from the other, as a fraction of
# the pasuk. 0.30 means “up to about a third slower or faster locally.”
ALIGN_BAND = 0.30
# Two correct takes are never sample-identical (mic noise, a slightly
# longer note). Agreement at or above this still means “got the trop.”
FULL_MATCH_CORRELATION = 0.75
# After we line two clips up, any two voices still share a little
# leftover wiggle (speech, breathing, a reciting tone). That is not
# trop. Only agreement above this counts toward the score.
CHANCE_CORRELATION = 0.50
# Farther than this from the teacher, after lining up, is a real miss
# (about two and a half piano keys), not tracker jitter.
OFF_TUNE_SEMITONES = 2.5
# Ignore one-off dots so a tiny wobble does not draw a red mark.
MIN_OFF_TUNE_POINTS = 3

# Pitch range we bother looking for (men, boys, and women testing the app).
MIN_PITCH_HZ = 70
MAX_PITCH_HZ = 500


def load_mono_wav(path):
    """Reads a WAV file as one channel of samples, plus how many per second."""
    audio, sample_rate = librosa.load(str(Path(path)), sr=None, mono=True)
    return audio, sample_rate


def estimate_pitch_hz(audio, sample_rate):
    """
    For each short slice, guess the pitch in Hz.

    librosa.pyin listens for a repeating sung note and also decides
    “is anyone actually voicing a note here?” Silence and consonants
    come back empty (NaN = “not a number”) so they do not invent a fake
    note. This is much less jumpy than a homemade wobble search.
    """
    pitch_hz, voiced_flag, _voiced_prob = librosa.pyin(
        audio,
        fmin=MIN_PITCH_HZ,
        fmax=MAX_PITCH_HZ,
        sr=sample_rate
    )
    if voiced_flag is not None:
        pitch_hz = numpy.where(voiced_flag, pitch_hz, numpy.nan)
    return numpy.asarray(pitch_hz, dtype=numpy.float64)


def _smooth(values, width):
    """Average neighboring dots so the line is a tune, not tracker noise."""
    if width < 2 or len(values) == 0:
        smoothed = numpy.array(values, dtype=numpy.float64)
    else:
        kernel = numpy.ones(width) / width
        smoothed = numpy.convolve(values, kernel, mode="same")
    return smoothed


def pitch_shape(audio, sample_rate):
    """
    Turns a recording into one trop line: COMPARISON_POINTS values.

    Each value is in semitones above/below that person's middle pitch, so
    a low voice and a high voice can draw the same up-down shape.
    Returns None if there is not enough voiced audio to trust.
    """
    pitch_hz = estimate_pitch_hz(audio, sample_rate)
    voiced_mask = numpy.isfinite(pitch_hz) & (pitch_hz > 0)
    voiced = pitch_hz[voiced_mask]
    shape = None

    if voiced.size >= MIN_VOICED_FRAMES:
        median_hz = numpy.median(voiced)
        semitones = numpy.full(pitch_hz.shape, numpy.nan)
        semitones[voiced_mask] = (
            SEMITONES_PER_OCTAVE * numpy.log2(voiced / median_hz)
        )
        # Keep only first sung note → last sung note. Silence at the ends
        # would otherwise get stretched and look like part of the trop.
        voiced_indices = numpy.flatnonzero(voiced_mask)
        sung = semitones[voiced_indices[0]:voiced_indices[-1] + 1]
        sung_voiced = numpy.isfinite(sung)
        filled = numpy.interp(
            numpy.arange(len(sung)),
            numpy.flatnonzero(sung_voiced),
            sung[sung_voiced]
        )
        filled = _smooth(filled, SMOOTH_WIDTH)
        sample_at = numpy.linspace(0, len(filled) - 1, COMPARISON_POINTS)
        shape = numpy.interp(sample_at, numpy.arange(len(filled)), filled)

    return shape


def _motion(shape):
    """How the trop is moving at each dot: up is positive, down is negative."""
    return numpy.diff(shape, prepend=shape[0])


def _align_student(teacher_shape, student_shape):
    """
    Slide the student's line so the same trop gestures sit over the teacher's.

    We match the *direction* of the tune (up vs down), not the raw height.
    Matching height alone can make a different trop look lined up. One take
    may pause or linger; ALIGN_BAND is how far that timing may drift.
    The student notes are then redrawn on the teacher's timeline.
    """
    teacher_motion = _motion(teacher_shape)
    student_motion = _motion(student_shape)
    cost, path = librosa.sequence.dtw(
        teacher_motion[None, :],
        student_motion[None, :],
        metric="euclidean",
        global_constraints=True,
        band_rad=ALIGN_BAND
    )
    if not numpy.isfinite(cost[-1, -1]):
        cost, path = librosa.sequence.dtw(
            teacher_motion[None, :],
            student_motion[None, :],
            metric="euclidean"
        )

    warped = numpy.full(len(teacher_shape), numpy.nan)
    counts = numpy.zeros(len(teacher_shape))
    for teacher_index, student_index in path:
        if numpy.isnan(warped[teacher_index]):
            warped[teacher_index] = student_shape[student_index]
            counts[teacher_index] = 1.0
        else:
            warped[teacher_index] += student_shape[student_index]
            counts[teacher_index] += 1.0

    known = counts > 0
    if known.any():
        warped[known] = warped[known] / counts[known]
        warped = numpy.interp(
            numpy.arange(len(teacher_shape)),
            numpy.flatnonzero(known),
            warped[known]
        )
    else:
        warped = numpy.array(student_shape, dtype=numpy.float64)
    return warped


def _corr(teacher_shape, student_shape):
    """
    How together the two lines wiggle: 1.0 = same ups and downs, 0.0 =
    unrelated, negative = one goes up while the other goes down.
    """
    teacher = teacher_shape - numpy.mean(teacher_shape)
    student = student_shape - numpy.mean(student_shape)
    denom = numpy.linalg.norm(teacher) * numpy.linalg.norm(student)
    value = 0.0
    if denom != 0:
        value = float(numpy.dot(teacher, student) / denom)
    return value


def _match_key(teacher_shape, student_shape):
    """
    Slide the student line up or down so both sit in the same key.

    A boy may start higher or lower than the teacher. That is not a trop
    mistake, so we subtract the typical leftover height after lining up.
    """
    offset = float(numpy.median(student_shape - teacher_shape))
    return student_shape - offset


def _off_tune_mask(teacher_shape, student_shape):
    """True on stretches where the boy left the teacher's tune."""
    far = numpy.abs(student_shape - teacher_shape) > OFF_TUNE_SEMITONES
    mask = numpy.zeros(len(far), dtype=bool)
    run_start = None
    for index, is_far in enumerate(far):
        if is_far:
            if run_start is None:
                run_start = index
        else:
            if run_start is not None and (index - run_start) >= MIN_OFF_TUNE_POINTS:
                mask[run_start:index] = True
            run_start = None
    if run_start is not None and (len(far) - run_start) >= MIN_OFF_TUNE_POINTS:
        mask[run_start:] = True
    return mask


def trop_score(teacher_shape, student_shape):
    """
    100 if the lined-up trop matches, even when voices, speed, or key
    differ. Random leftover agreement between two voices does not count.
    """
    agreement = _corr(teacher_shape, student_shape)
    usable = FULL_MATCH_CORRELATION - CHANCE_CORRELATION
    percent = 0.0
    if usable > 0:
        percent = 100.0 * (agreement - CHANCE_CORRELATION) / usable
    return max(0.0, min(100.0, percent))


def compare_trop(teacher_path, student_path):
    """
    Compares trop (pitch shape) of two recordings.
    Returns a dict with teacher_shape, student_shape, score, and
    off_tune (where the student left the tune), or None if either clip
    has too little voiced audio.
    The student shape is already lined up in time and key for drawing.
    """
    teacher_audio, teacher_rate = load_mono_wav(teacher_path)
    student_audio, student_rate = load_mono_wav(student_path)
    teacher_shape = pitch_shape(teacher_audio, teacher_rate)
    student_shape = pitch_shape(student_audio, student_rate)
    comparison = None
    if teacher_shape is not None and student_shape is not None:
        aligned_student = _match_key(
            teacher_shape, _align_student(teacher_shape, student_shape))
        comparison = {
            "teacher_shape": teacher_shape,
            "student_shape": aligned_student,
            "score": trop_score(teacher_shape, aligned_student),
            "off_tune": _off_tune_mask(teacher_shape, aligned_student)
        }
    return comparison
