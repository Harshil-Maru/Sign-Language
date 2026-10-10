from gtts import gTTS
import os

# Gujarati translations of your labels
guj_map = {
    "Hello": "નમસ્તે",
    "Yes": "હા",
    "No": "ના",
    "Thanks": "આભાર",
    "IloveYou": "હું તને પ્રેમ કરું છું",
    "Please": "કૃપા કરીને",
}

# Output folder
out_dir = "audio_gujarati"
os.makedirs(out_dir, exist_ok=True)

# Generate Gujarati audios
for label, text in guj_map.items():
    tts = gTTS(text=text, lang='gu')
    filename = os.path.join(out_dir, f"{label}.mp3")
    tts.save(filename)
    print(f"Saved Gujarati audio: {filename}")
