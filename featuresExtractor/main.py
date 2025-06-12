import librosa
import numpy as np
import json
import os

def analyze_audio(file_path, output_json):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Tempo and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()
    if len(tempo)!=1:
        raise ValueError("something is wrong")
    tempo = tempo[0]
    # Onset detection
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr).tolist()

    # Amplitude envelope (RMS)
    frame_length = 2048
    hop_length = 512
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length).tolist()
    amplitude_envelope = list(rms)
    
    amplitude_envelope = [float(x) for x in amplitude_envelope]

    # Frequency spectrum (average over time using STFT)
    stft = np.abs(librosa.stft(y, n_fft=2048))
    #n_fft is How many audio samples are used in each chunk/window -> how detailed the frequency analysis is
    #n_fft = 2048 is  Finer frequency detail but Slower response
    freqs = librosa.fft_frequencies(sr=sr)
    avg_spectrum = np.mean(stft, axis=1).tolist()
    frequencies = freqs.tolist()

    # Output as JSON
    data = {
        "tempo": tempo,
        "beats": beat_times,
        "onsets": onset_times,
        "amplitude_envelope": {
            "times": times,
            "values": amplitude_envelope
        },
        "frequencies": {
            "hz": frequencies,
            "average_amplitudes": avg_spectrum
        }
    }

    # Write to JSON
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Analysis complete. JSON saved to {output_json}")

# Example usage
if __name__ == "__main__":
    mp3_file = "Bayern, Des Samma Mia - Bavarian Folk Song [Lyrics  Translation].mp3"
    json_output = "your_song_analysis.json"
    analyze_audio(mp3_file, json_output)
