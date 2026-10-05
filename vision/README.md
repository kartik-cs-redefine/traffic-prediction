# vision

Owner: Kartik

Detects and tracks vehicles (YOLOv8 + ByteTrack), counts line crossings and writes window-wise traffic features.

## Setup
```
cd vision
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run
1. Put videos in `vision/videos/` (git-ignored).
2. Edit the settings at the top of `batch.py` (`VIDEOS`, `WINDOW_SEC`, `SKIP`).
3. `PREVIEW_ONLY = True` -> check line/ROI previews in `previews/`.
4. `PREVIEW_ONLY = False` -> `python batch.py`. Per-video CSVs go to `out/`, merged file to `all_features.csv`.

## Input / output
- Input: video files.
- Output: features CSV following `docs/data_contract.md`.

## Known limitations
Speed is uncalibrated; ID switching and overlap lower counts in heavy traffic; trained on Iowa highway scenes, not mixed Indian traffic.
