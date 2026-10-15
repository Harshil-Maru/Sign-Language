import os

try:
    from gtts import gTTS
except ImportError:  # pragma: no cover - failures are reported during setup.
    gTTS = None

# List of your 6 labels
labels = ["Hello", "Yes", "No", "Thanks", "IloveYou", "Please"]


def generate_english_audio():
    if gTTS is None:
        raise RuntimeError("gTTS is required to generate audio files.")

    os.makedirs("audio", exist_ok=True)
    for label in labels:
        tts = gTTS(text=label, lang="en")
        filename = f"audio/{label}.mp3"
        tts.save(filename)
        print(f"Saved: {filename}")


if __name__ == "__main__":
    generate_english_audio()
