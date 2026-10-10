from ultralytics import YOLO
import pygame
import time
import threading
import RPi.GPIO as GPIO

# --- GPIO Setup ---
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Load YOLO model ---
model = YOLO("runs/detect/train/weights/best.pt")

# --- Audio maps for each language ---
audio_map_en = {
    "Hello": "audio/en/Hello.mp3",
    "Yes": "audio/en/Yes.mp3",
    "No": "audio/en/No.mp3",
    "Thanks": "audio/en/Thanks.mp3",
    "IloveYou": "audio/en/IloveYou.mp3",
    "Please": "audio/en/Please.mp3",
}

audio_map_hi = {
    "Hello": "audio/hi/Hello.mp3",
    "Yes": "audio/hi/Yes.mp3",
    "No": "audio/hi/No.mp3",
    "Thanks": "audio/hi/Thanks.mp3",
    "IloveYou": "audio/hi/IloveYou.mp3",
    "Please": "audio/hi/Please.mp3",
}

audio_map_gu = {
    "Hello": "audio/gu/Hello.mp3",
    "Yes": "audio/gu/Yes.mp3",
    "No": "audio/gu/No.mp3",
    "Thanks": "audio/gu/Thanks.mp3",
    "IloveYou": "audio/gu/IloveYou.mp3",
    "Please": "audio/gu/Please.mp3",
}

# --- Language setup ---
languages = [audio_map_en, audio_map_hi, audio_map_gu]
lang_names = ["English", "Hindi", "Gujarati"]
current_lang_index = 0
audio_map = languages[current_lang_index]

# --- Init pygame mixer ---
pygame.mixer.init()

last_spoken = None
last_time = 0
cooldown = 2  # seconds

def play_audio(file):
    """Play audio in a background thread so detection loop is not blocked."""
    def _play():
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    threading.Thread(target=_play, daemon=True).start()

def button_callback(channel):
    """Cycle language when button is pressed."""
    global current_lang_index, audio_map
    current_lang_index = (current_lang_index + 1) % len(languages)
    audio_map = languages[current_lang_index]
    print(f"🔄 Language changed to: {lang_names[current_lang_index]}")

# --- Setup button event ---
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=500)

print("✅ Sign Language Detection Started")
print(f"📷 Camera initialized. Current language: {lang_names[current_lang_index]}")
print("👉 Press the button to change language (English → Hindi → Gujarati → English...)")

# --- Run detection with webcam ---
for result in model.predict(source=0, conf=0.25, imgsz=256, show=True, stream=True):
    boxes = result.boxes
    if boxes is not None and len(boxes) > 0:
        class_ids = boxes.cls.cpu().numpy().astype(int)
        for cls in class_ids:
            label = model.names[cls]
            current_time = time.time()

            if label in audio_map and (label != last_spoken or (current_time - last_time) > cooldown):
                print(f"✅ Detected: {label} → Playing in {lang_names[current_lang_index]}")
                play_audio(audio_map[label])
                last_spoken = label
                last_time = current_time
