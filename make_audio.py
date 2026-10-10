from gtts import gTTS
import os

# List of your 6 labels
labels = ["Hello", "Yes", "No", "Thanks", "IloveYou", "Please"]

# Create folder for audio if not exists
os.makedirs("audio", exist_ok=True)

# Generate audio files
for label in labels:
    tts = gTTS(text=label, lang="en")
    filename = f"audio/{label}.mp3"
    tts.save(filename)
    print(f"Saved: {filename}")