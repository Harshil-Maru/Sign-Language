import importlib.util
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_dataset_configuration_matches_labels():
    config_path = ROOT / "data" / "data.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    assert data["train"] == "../train/images"
    assert data["val"] == "../test/images"
    assert data["nc"] == 6
    assert data["names"] == ["Hello", "IloveYou", "No", "Please", "Thanks", "Yes"]

    assert (ROOT / "data" / "train" / "images").exists()
    assert (ROOT / "data" / "test" / "images").exists()


def test_model_weight_file_exists_and_loads():
    from ultralytics import YOLO

    model_path = ROOT / "runs" / "detect" / "train" / "weights" / "best.pt"
    assert model_path.exists()
    model = YOLO(str(model_path))
    assert model.names == {0: "Hello", 1: "IloveYou", 2: "No", 3: "Please", 4: "Thanks", 5: "Yes"}


def test_supported_language_audio_maps_exist():
    spec = importlib.util.spec_from_file_location("detect_app", ROOT / "detect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    english = module.get_audio_maps()["English"]
    assert set(english) == {"Hello", "IloveYou", "No", "Please", "Thanks", "Yes"}

    for label, path in english.items():
        assert (ROOT / path).exists(), f"Missing English audio for {label}: {path}"

    hindi = module.get_audio_maps()["Hindi"]
    for label, path in hindi.items():
        assert (ROOT / path).exists(), f"Missing Hindi audio for {label}: {path}"

    gujarati = module.get_audio_maps()["Gujarati"]
    for label, path in gujarati.items():
        assert (ROOT / path).exists(), f"Missing Gujarati audio for {label}: {path}"


def test_invalid_language_raises_value_error():
    spec = importlib.util.spec_from_file_location("detect_app", ROOT / "detect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        module._audio_map_for_language("fr")
        raise AssertionError("Expected ValueError for unsupported language.")
    except ValueError:
        pass
