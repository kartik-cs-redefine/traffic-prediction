# AI-Based Predictive Traffic Management System

Camera video -> vehicle detection -> traffic features -> current classification -> 15-min congestion forecast -> dashboard alerts -> alternative route.

## Pipeline
```
Video -> vision -> features (CSV/DB) -> current_ml -> forecasting -> backend API -> frontend -> routing
```
Details: [docs/architecture.md](docs/architecture.md) | Data format: [docs/data_contract.md](docs/data_contract.md)

## Repository layout
| Folder | What lives here | Owner |
|---|---|---|
| `vision/` | Detection, tracking, counting, feature extraction (YOLOv8 + ByteTrack) | Kartik |
| `data_pipeline/` | DB schema, loaders, synthetic data generator | Kshitij |
| `data/` | Datasets (`processed/` committed, `raw/` never committed) | Kshitij |
| `current_ml/` | Low/Moderate/Heavy/Severe classifier | Avantika |
| `forecasting/` | 15-min prediction model and probabilities | Kanika |
| `backend/` | FastAPI endpoints | Krish |
| `frontend/` | Dashboard / GCS | Krish |
| `routing/` | Map and alternative route module | Krishna |
| `hardware/` | Camera / edge setup notes and scripts | Krishna |
| `docs/` | Architecture, data contract, API docs | Everyone |

## Getting started
Each module has its own `README.md` and `requirements.txt`. Use one virtual environment per module:
```
cd <module>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Rules
Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first commit.
