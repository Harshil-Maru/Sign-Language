from gtts import gTTS
import os

# Hindi + Gujarati translations
phrases_hi = {
    "Hello": "नमस्ते",
    "Yes": "हाँ",
    "No": "नहीं",
    "Thanks": "धन्यवाद",
    "IloveYou": "मैं तुमसे प्यार करता हूँ",  # change करता हूँ → करती हूँ if female
    "Please": "कृपया"
}

phrases_gu = {
    "Hello": "નમસ્તે",
    "Yes": "હા",
    "No": "ના",
    "Thanks": "આભાર",
    "IloveYou": "હું તને પ્રેમ કરું છું",
    "Please": "કૃપા કરીને"
}

langs = {
    "hi": phrases_hi,
    "gu": phrases_gu
}

for code, phrases in langs.items():
    os.makedirs(f"audio/{code}", exist_ok=True)
    print(f"🔄 Generating {code} audios...")
    for key, text in phrases.items():
        try:
            tts = gTTS(text=text, lang=code)
            filepath = f"audio/{code}/{key}.mp3"
            tts.save(filepath)
            print(f"✅ Saved: {filepath}")
        except Exception as e:
            print(f"⚠️ Error for {key} in {code}: {e}")
