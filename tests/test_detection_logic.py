import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("detect_app", ROOT / "detect.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeGPIO:
    BCM = "BCM"
    IN = "IN"
    PUD_UP = "PUD_UP"
    FALLING = "FALLING"

    def __init__(self):
        self.calls = []

    def setmode(self, mode):
        self.calls.append(("setmode", mode))

    def setup(self, pin, mode, pull_up_down=None):
        self.calls.append(("setup", pin, mode, pull_up_down))

    def add_event_detect(self, pin, edge, callback=None, bouncetime=500):
        self.calls.append(("add_event_detect", pin, edge, callback, bouncetime))


def test_should_play_reduces_duplicate_signs():
    assert module.should_play("Hello", None, 10.0, 0.0, cooldown=2.0) is True
    assert module.should_play("Hello", "Hello", 10.0, 0.0, cooldown=2.0) is True
    assert module.should_play("Hello", "Hello", 1.5, 0.0, cooldown=2.0) is False
    assert module.should_play("Unknown", "Unknown", 1.0, 0.0, cooldown=2.0) is False


def test_process_detection_returns_valid_state():
    audio_map = module._audio_map_for_language("en")
    should_play, last_spoken, last_time = module.process_detection_result(
        "Hello", audio_map, None, 0.0, 10.0, cooldown=2.0
    )
    assert should_play is True
    assert last_spoken == "Hello"
    assert last_time == 10.0


def test_gpio_initialization_works_with_mocked_pins():
    fake_gpio = FakeGPIO()
    gpio = module.initialize_gpio(button_pin=17, gpio_module=fake_gpio)
    assert gpio is fake_gpio
    assert any(call[0] == "setmode" for call in fake_gpio.calls)
    assert any(call[0] == "setup" for call in fake_gpio.calls)


def test_invalid_label_type_raises_type_error():
    with pytest.raises(TypeError):
        module.should_play(123, None, 1.0, 0.0)
