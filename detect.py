import os
import threading
import time

try:
    import pygame
except ImportError:  # pragma: no cover - handled in runtime validation and tests.
    pygame = None

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - handled in runtime validation and tests.
    YOLO = None

SUPPORTED_SIGN_LABELS = ["Hello", "IloveYou", "No", "Please", "Thanks", "Yes"]
BUTTON_PIN = 17
COOLDOWN_SECONDS = 2.0


def _audio_map_for_language(language_key):
    language_key = (language_key or "en").lower()
    language_map = {
        "en": {
            "Hello": os.path.join("audio", "en", "Hello.mp3"),
            "Yes": os.path.join("audio", "en", "Yes.mp3"),
            "No": os.path.join("audio", "en", "No.mp3"),
            "Thanks": os.path.join("audio", "en", "Thanks.mp3"),
            "IloveYou": os.path.join("audio", "en", "IloveYou.mp3"),
            "Please": os.path.join("audio", "en", "Please.mp3"),
        },
        "hi": {
            "Hello": os.path.join("audio", "hi", "Hello.mp3"),
            "Yes": os.path.join("audio", "hi", "Yes.mp3"),
            "No": os.path.join("audio", "hi", "No.mp3"),
            "Thanks": os.path.join("audio", "hi", "Thanks.mp3"),
            "IloveYou": os.path.join("audio", "hi", "IloveYou.mp3"),
            "Please": os.path.join("audio", "hi", "Please.mp3"),
        },
        "gu": {
            "Hello": os.path.join("audio", "gu", "Hello.mp3"),
            "Yes": os.path.join("audio", "gu", "Yes.mp3"),
            "No": os.path.join("audio", "gu", "No.mp3"),
            "Thanks": os.path.join("audio", "gu", "Thanks.mp3"),
            "IloveYou": os.path.join("audio", "gu", "IloveYou.mp3"),
            "Please": os.path.join("audio", "gu", "Please.mp3"),
        },
    }
    if language_key not in language_map:
        raise ValueError(f"Unsupported language '{language_key}'. Supported: {sorted(language_map)}")
    return language_map[language_key]


def get_audio_maps():
    return {
        "English": _audio_map_for_language("en"),
        "Hindi": _audio_map_for_language("hi"),
        "Gujarati": _audio_map_for_language("gu"),
    }


def initialize_gpio(button_pin=BUTTON_PIN, gpio_module=None):
    """Attach the Raspberry Pi GPIO interface when it is available."""
    if gpio_module is not None:
        gpio = gpio_module
    else:
        try:
            import RPi.GPIO as GPIO
        except ImportError:
            return None
        gpio = GPIO

    gpio.setmode(gpio.BCM)
    gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    return gpio


def initialize_audio_mixer():
    if pygame is None:
        raise RuntimeError("pygame is required for audio playback.")
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    return pygame.mixer


def play_audio(file_path):
    """Play audio in a background thread so detection is not blocked."""
    if pygame is None:
        raise RuntimeError("pygame is required for audio playback.")

    def _play():
        mixer = initialize_audio_mixer()
        mixer.music.load(file_path)
        mixer.music.play()

    threading.Thread(target=_play, daemon=True).start()


def should_play(label, last_spoken, current_time, last_time, cooldown=COOLDOWN_SECONDS):
    if not isinstance(label, str):
        raise TypeError("label must be a string or None")
    if label not in SUPPORTED_SIGN_LABELS:
        return False
    if last_spoken is None:
        return True
    if label != last_spoken:
        return True
    return (current_time - last_time) > cooldown


def process_detection_result(label, audio_map, last_spoken, last_time, current_time, cooldown=COOLDOWN_SECONDS):
    if label not in audio_map:
        return False, last_spoken, last_time
    if not should_play(label, last_spoken, current_time, last_time, cooldown):
        return False, last_spoken, last_time
    return True, label, current_time


def build_model(model_path="runs/detect/train/weights/best.pt"):
    if YOLO is None:
        raise RuntimeError("ultralytics is required to load the YOLO model.")
    return YOLO(model_path)


def main():
    languages = [
        _audio_map_for_language("en"),
        _audio_map_for_language("hi"),
        _audio_map_for_language("gu"),
    ]
    lang_names = ["English", "Hindi", "Gujarati"]
    current_lang_index = 0
    audio_map = languages[current_lang_index]
    last_spoken = None
    last_time = 0.0

    gpio = initialize_gpio(BUTTON_PIN)

    def button_callback(channel):
        nonlocal current_lang_index, audio_map
        current_lang_index = (current_lang_index + 1) % len(languages)
        audio_map = languages[current_lang_index]
        print(f"🔄 Language changed to: {lang_names[current_lang_index]}")

    if gpio is not None:
        gpio.add_event_detect(BUTTON_PIN, gpio.FALLING, callback=button_callback, bouncetime=500)

    print("✅ Sign Language Detection Started")
    print(f"📷 Camera initialized. Current language: {lang_names[current_lang_index]}")
    print("👉 Press the button to change language (English → Hindi → Gujarati → English...)")

    model = build_model()
    initialize_audio_mixer()

    for result in model.predict(source=0, conf=0.25, imgsz=256, show=True, stream=True):
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            continue

        class_ids = boxes.cls.cpu().numpy().astype(int)
        for cls in class_ids:
            label = model.names[int(cls)]
            current_time = time.time()
            should_emit, last_spoken, last_time = process_detection_result(
                label, audio_map, last_spoken, last_time, current_time, cooldown=COOLDOWN_SECONDS
            )
            if not should_emit:
                continue
            print(f"✅ Detected: {label} → Playing in {lang_names[current_lang_index]}")
            play_audio(audio_map[label])


if __name__ == "__main__":
    main()
