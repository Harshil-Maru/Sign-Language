import os

try:
    from gtts import gTTS
except ImportError:  # pragma: no cover - failures are reported during setup.
    gTTS = None

# Gujarati translations of your labels
guj_map = {
    "Hello": "નમસ્તે",
    "Yes": "હા",
    "No": "ના",
    "Thanks": "આભાર",
    "IloveYou": "હું તને પ્રેમ કરું છું",
    "Please": "કૃપા કરીને",
}


def generate_gujarati_audio(out_dir="audio_gujarati"):
    if gTTS is None:
        raise RuntimeError("gTTS is required to generate Gujarati audio files.")

    os.makedirs(out_dir, exist_ok=True)
    for label, text in guj_map.items():
        tts = gTTS(text=text, lang="gu")
        filename = os.path.join(out_dir, f"{label}.mp3")
        tts.save(filename)
        print(f"Saved Gujarati audio: {filename}")


if __name__ == "__main__":
    generate_gujarati_audio()
