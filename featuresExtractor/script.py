import librosa, numpy as np, sys, pathlib, os

# --- edit just these two lines -----------------------------------
AUDIO_FILE = "Bayern, Des Samma Mia - Bavarian Folk Song [Lyrics  Translation].mp3"          # wav, mp3, flac … anything librosa can open
OUT_FILE   = "beats.npy"           # will be created next to this script
# -----------------------------------------------------------------

print("CWD :", os.getcwd())
print("Exists?", pathlib.Path(AUDIO_FILE).resolve().exists())

y, sr      = librosa.load(AUDIO_FILE)
tempo, beat_idx = librosa.beat.beat_track(y=y, sr=sr, trim=False)

beat_times = librosa.frames_to_time(beat_idx, sr=sr)   # seconds
np.save(OUT_FILE, beat_times)

print(f"✔ Saved {len(beat_times)} beats to {pathlib.Path(OUT_FILE).resolve()}")