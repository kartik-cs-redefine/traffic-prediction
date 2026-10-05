# Data

- `processed/all_features.csv`: features from 12 videos (AI City Challenge 2021 Track 4, Iowa DOT highway cameras), 5 s windows. Produced by `vision/batch.py`.
- `processed/previews/`: count line (red) and ROI top (blue) used for each camera.
- `raw/`: original videos. Never committed (see .gitignore). Download link: <add Drive link here>.

Known notes: video 66 may have unreliable `car_count`; videos 1, 11, 56, 96 are heavy traffic; video 16 is almost empty. See `docs/data_contract.md`.
