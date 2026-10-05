# Data Contract (shared by all modules)

## Features table (produced by `vision`)
| Column | Meaning |
|---|---|
| video_id | Source camera / video id (each id is a different camera) |
| timestamp | End time of the window (ISO 8601). Assumed for recorded videos |
| car_count | Unique cars + trucks inside the ROI during the window |
| bus_count | Unique buses inside the ROI |
| bike_count | Unique motorcycles inside the ROI |
| avg_speed | Relative speed from pixel movement. Scale is arbitrary (not calibrated), not comparable across cameras |
| density | Average vehicles in the ROI per frame |
| occupancy | Share of ROI area covered by vehicle boxes |
| flow | Vehicles crossing the count line, scaled to per minute |

Window length: 5 seconds. `flow` is noisy at this size (one vehicle = 12/min); aggregate to 30 s or 1 min if needed.

## Traffic levels
`0 = Low, 1 = Moderate, 2 = Heavy, 3 = Severe`

## Rules
- Treat each `video_id` as its own time series. Do not concatenate different cameras.
- Set thresholds per camera; density, occupancy and avg_speed are not comparable across cameras.
- Evaluate with a time-based split, never a random split.

## API shapes (owned by backend)
`GET /current-traffic`
```json
{"timestamp": "...", "total_vehicles": 64, "level": "Moderate"}
```
`GET /prediction`
```json
{"horizon_min": 15, "probs": {"low": 0.08, "moderate": 0.14, "heavy": 0.78, "severe": 0.0}, "predicted": "Heavy"}
```
