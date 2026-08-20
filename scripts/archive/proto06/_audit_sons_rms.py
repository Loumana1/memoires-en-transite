#!/usr/bin/env python3
"""Outil dev: audit RMS par seconde des segments SONS/ (détection de silences).

Signale tout segment contenant >2 s consécutives sous le seuil, ainsi que les
intros silencieuses. Lecture WAV PCM 16 bits via le module wave (stdlib).
"""
import array
import glob
import math
import os
import wave


def rms16(frames):
    a = array.array("h")
    a.frombytes(frames[: len(frames) // 2 * 2])
    if not a:
        return 0
    return math.sqrt(sum(x * x for x in a) / len(a))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
THRESH = 150  # RMS 16 bits ~ -47 dBFS

for path in sorted(glob.glob(os.path.join(ROOT, "SONS", "*", "*", "*.wav"))):
    rel = os.path.relpath(path, ROOT)
    try:
        w = wave.open(path, "rb")
    except Exception as exc:
        print(f"ILLISIBLE {rel}: {exc}")
        continue
    sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    nsec = w.getnframes() // sr
    quiet = []
    for s in range(max(nsec, 1)):
        frames = w.readframes(sr)
        if not frames:
            break
        quiet.append(rms16(frames) < THRESH)
    w.close()
    # plages silencieuses consecutives
    runs, start = [], None
    for i, q in enumerate(quiet):
        if q and start is None:
            start = i
        if not q and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(quiet)))
    bad = [r for r in runs if r[1] - r[0] >= 2]
    intro = runs[0] if runs and runs[0][0] == 0 else None
    if bad or intro:
        msg = " ".join(f"[{a}-{b}s]" for a, b in bad)
        print(f"SILENCES {rel} (duree {len(quiet)}s): {msg}")
