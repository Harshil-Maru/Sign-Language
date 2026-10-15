# Sign Language Recognition and Speech Output

This repository contains a YOLOv8-based sign language recognition project for six static signs: `Hello`, `IloveYou`, `No`, `Please`, `Thanks`, and `Yes`. The application captures frames from a camera, detects the sign, maps the detected class to a phrase, and plays the matching audio in English, Hindi, or Gujarati.

## Problem statement

People who are deaf or hard-of-hearing often rely on visual communication. A lightweight real-time sign recognizer can translate common gestures into spoken output, which improves communication with non-sign-language users and helps bridge accessibility gaps in classrooms, clinics, kiosks, and public-facing services.

## Project goals

- Detect the six supported signs in real time from a webcam or Raspberry Pi camera.
- Map each class to a phrase and play the corresponding spoken audio.
- Support language switching between English, Hindi, and Gujarati.
- Provide a reproducible dataset and training workflow for model evaluation.
- Document the system architecture and testing process for official review.

## Features

- YOLOv8 object detection for six sign classes.
- Audio output using `pygame`.
- Optional GPIO button support for language switching on Raspberry Pi devices.
- Pretrained detection weights at `runs/detect/train/weights/best.pt`.
- Validation metrics in `runs/detect/train/results.csv`.
- Generated audio files under `audio/en`, `audio/hi`, and `audio/gu`.

## Current limitations

- The system is validated on the provided six-sign vocabulary only.
- Real-world performance depends on camera quality, lighting, and background complexity.
- The trained metrics are validation metrics from the included training run, not a measured deployment study.
- The code is designed for desktop development and Raspberry Pi deployment, but the GPIO interface is optional and only relevant on Raspberry Pi hardware.

## Supported sign vocabulary and languages

Signs:

- Hello
- IloveYou
- No
- Please
- Thanks
- Yes

Languages:

- English
- Hindi
- Gujarati

## Repository structure

```text
sign/
├── audio/
│   ├── en/
│   ├── hi/
│   └── gu/
├── data/
│   ├── data.yaml
│   ├── train/
│   └── test/
├── runs/
│   └── detect/train/
├── detect.py
├── make_audio.py
├── guj.py
├── requirements.txt
├── requirements-pi.txt
├── LICENSE
├── README.md
├── docs/
│   ├── TECHNICAL_DESIGN.md
│   └── TEST_REPORT.md
├── tests/
├── yolov8n.pt
└── demo video.mp4
```

## Prerequisites

- Python 3.10+ recommended; this environment was validated with Python 3.13.7.
- A webcam or Raspberry Pi camera connected to the host.
- Audio output device.
- Optional: Raspberry Pi + GPIO button for language switching.

## Installation

Create and activate a virtual environment.

On Windows PowerShell:

```powershell
cd C:\Users\maruh\Downloads\sign
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Linux or macOS:

```bash
cd /path/to/sign
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For Raspberry Pi deployment, use:

```bash
pip install -r requirements-pi.txt
```

## Model setup and verification

The repository includes a trained model at `runs/detect/train/weights/best.pt`.

Verify that the model loads correctly:

```bash
python -c "from ultralytics import YOLO; model = YOLO('runs/detect/train/weights/best.pt'); print(model.names)"
```

The expected class map is:

```python
{0: 'Hello', 1: 'IloveYou', 2: 'No', 3: 'Please', 4: 'Thanks', 5: 'Yes'}
```

This matches `data/data.yaml`.

## Running the application

From the project root:

```bash
python detect.py
```

This starts the webcam stream and plays the detected sign in the active language. The current language is English by default. Press the GPIO button, when connected, to cycle through English, Hindi, and Gujarati.

## Audio generation

The repository already includes MP3 files under `audio/`. To regenerate them, use:

```bash
python make_audio.py
```

This creates the English audio directory. For Gujarati, run:

```bash
python guj.py
```

The Hindi audio files are supplied as part of the repository and can be reused without a dedicated generator script.

## Dataset and model evaluation

The dataset is configured in `data/data.yaml` and uses the following structure:

```yaml
train: ../train/images
val: ../test/images
nc: 6
names: ['Hello', 'IloveYou', 'No', 'Please', 'Thanks', 'Yes']
```

Training metrics are recorded in `runs/detect/train/results.csv`.

Measured validation metrics from the final training epoch:

- Precision(B): 0.98819
- Recall(B): 1.0
- mAP@0.5(B): 0.995
- mAP@0.5:0.95(B): 0.39403

These are training-validation values, not a real-world field accuracy claim.

## Raspberry Pi deployment

This project was written to support Raspberry Pi deployment. The code path includes GPIO support for a button that changes the active language. To use this functionality:

- Connect a button to GPIO pin 17.
- Use the Raspberry Pi GPIO library via `requirements-pi.txt`.
- Run the app with a Pi camera or USB camera.

The GPIO code is optional and is only used when the hardware is present.

## Troubleshooting

- If `RPi.GPIO` is missing on a non-Pi computer, the app will still import, but GPIO input is unavailable.
- If `pygame` is missing, install `requirements.txt` before running the detection app.
- If `gTTS` is missing, install `requirements.txt` or regenerate the audio as needed.
- If the model path is missing or broken, check that `runs/detect/train/weights/best.pt` exists.
- If the audio files are missing, check the `audio/<language>/<label>.mp3` paths.

## Documentation

- Technical design: `docs/TECHNICAL_DESIGN.md`
- Test report: `docs/TEST_REPORT.md`

## License

This project is distributed under the MIT License. The license file in this repository covers the source code and documentation. It does not automatically cover third-party model weights, datasets, or other copyrighted audio/media unless the original asset owners explicitly permit redistribution under the same terms.

## Environment variables

No runtime environment variables are required for this project.
