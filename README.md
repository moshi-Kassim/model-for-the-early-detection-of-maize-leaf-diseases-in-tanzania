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

**Option 1 — Double-click (Windows):**
```
run.bat
```

**Option 2 — Command line:**
```bash
cd "python dashboard"
streamlit run app.py
```

The app **auto-loads** the AI model and database on startup. Diagnosis runs **automatically** when you upload an image.

The app opens in your browser at `http://localhost:8501`.

## Usage

1. Open the **Diagnose** page
2. Upload a maize leaf image (JPG/PNG) or use a sample image
3. View the predicted disease class and confidence score
4. Check **Diagnosis History** for saved records in the database

## Database

SQLite database stores every diagnosis attempt locally.

```bash
python database/init_db.py
```

**Table: `diagnoses`**

| Column | Description |
|---|---|
| id | Auto-increment primary key |
| created_at | UTC timestamp |
| image_filename | Original file name |
| image_path | Saved copy path (uploads only) |
| predicted_class | Model class key |
| display_name | Human-readable disease name |
| confidence | Confidence score (%) |
| status | `accepted` or `rejected` |
| rejection_reason | Why upload was rejected |
| probabilities_json | All class probabilities |
| source | `upload` or `sample` |

Database file: `database/maize_diagnosis.db`

## Project structure

```
python dashboard/
├── app.py                  # Streamlit dashboard
├── requirements.txt
├── model/
│   └── corn_disease_cnn.h5 # Trained Custom CNN (92.37% test accuracy)
├── database/
│   ├── db.py                  # SQLite operations
│   ├── init_db.py             # Create database manually
│   ├── maize_diagnosis.db     # Auto-created database file
│   └── uploads/               # Saved uploaded images
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
