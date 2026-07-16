# Maize Leaf Disease Detection Dashboard

Streamlit web dashboard for real-time diagnosis of maize leaf diseases using a trained Custom CNN model.

## Project

**Developing a Predictive Deep Learning Model for the Early Detection of Maize Leaf Diseases in Tanzania**

Detects four classes:
- Healthy
- Common Rust (*Puccinia sorghi*)
- Northern Leaf Blight (*Exserohilum turcicum*)
- Cercospora Leaf Spot (*Cercospora zeae-maydis*)

## Requirements

- Python 3.10+
- Trained model: `model/corn_disease_cnn.h5` (included)

## Setup

```bash
cd "python dashboard"
pip install -r requirements.txt
```

## Run the dashboard

There are **two separate apps**:

| Dashboard | File | Port | For |
|---|---|---|---|
| **User Dashboard** | `user_app.py` | 8501 | Farmers — upload, top disease, management only |
| **Admin Dashboard** | `app.py` | 8502 | Technical — detailed diagnosis, metrics, about |

**User Dashboard (farmers):**
```bash
streamlit run user_app.py
```
Or double-click `run_user.bat` / `run.bat`

**Admin Dashboard (technical):**
```bash
streamlit run app.py --server.port 8502
```
Or double-click `run_admin.bat`

- User app: `http://localhost:8501`
- Admin app: `http://localhost:8502`

Both apps **auto-load** the AI model on startup. Diagnosis runs **automatically** when you upload an image.

## Usage

**User Dashboard**
1. Upload a maize leaf image (JPG/PNG)
2. View the detected disease and recommended management

**Admin Dashboard**
1. Open **Diagnose** and upload a real maize leaf image for full probabilities and symptoms
2. Open **Performance** for model evaluation metrics
3. Open **About** for project information

> For panel presentation, use **live uploads only** (no pre-loaded sample images). Sample files in `assets/sample_images/` are kept for local developer testing only.

## Project structure

```
python dashboard/
├── user_app.py             # User dashboard (farmers)
├── app.py                  # Admin dashboard (technical)
├── run_user.bat            # Start user app (port 8501)
├── run_admin.bat           # Start admin app (port 8502)
├── requirements.txt
├── utils/
│   └── dashboard_core.py   # Shared model and diagnosis logic
├── model/
│   └── corn_disease_cnn.h5 # Trained Custom CNN (92.37% test accuracy)
├── assets/
│   └── sample_images/      # Demo images per class
└── data/                   # Notebooks, PDF, and original model files
```

## Model details

| Property | Value |
|---|---|
| Architecture | Custom CNN |
| Input size | 128 × 128 × 3 |
| Test accuracy | 92.37% |
| Classes | 4 |
| Framework | TensorFlow / Keras |

## Team

EASTC Bachelor of Data Science Year III — Academic Year 2025/2026
