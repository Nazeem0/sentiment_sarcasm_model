
# Sentiment & Sarcasm Analysis System

A modern, full-stack web application designed to classify sentiment (Positive, Negative) and detect Sarcasm in text data. This project features a Flask-powered backend using transformer-based models and a premium, responsive frontend for real-time interaction and batch processing.

## 🚀 Features

- **Real-time Sentiment Testing**: Instantly test individual sentences for sentiment and sarcasm with confidence scores.
- **Batch CSV Processing**: Upload CSV datasets of reviews to categorize them automatically.
- **Visual Dashboard**: A sleek, dark-themed dashboard with animated transitions and intuitive data visualization.
- **Sarcasm Detection**: Specialized logic to differentiate between genuine sentiment and sarcastic remarks.
- **Synthetic Data Generation**: Includes a tool to generate realistic mobile phone reviews for testing.

## 🛠️ Tech Stack

- **Frontend**: Vanilla JS, CSS3 (Glassmorphism, CSS Variables), HTML5.
- **Backend**: Python, Flask, Flask-CORS.
- **ML Engine**: HuggingFace Transformers (BERT/RoBERTa based), Pandas.
- **Data**: CSV-based processing pipeline.

## 📂 Project Structure

```text
├── database_creator/       # Tools for generating synthetic review datasets
│   └── database_creator.py
├── frontend/               # Web interface (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── ml_model/               # Flask API and ML logic
│   ├── app.py             # Main API server
│   ├── model.ipynb        # Model training/exploration notebook
│   └── review.csv         # Sample dataset
└── .gitignore             # Git exclusion rules
```

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nazeem0/sentiment_sarcasm_model.git
cd sentiment_sarcasm_model
```

### 2. Set up Python Environment
```bash
python -m venv venv
source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
pip install flask flask-cors pandas transformers torch
```

### 3. Model Placement
The application expects a fine-tuned model in `ml_model/sentiment_sarcasm_model/`. If you are using a custom model, ensure the path in `app.py` matches your directory structure.

## 🚦 How to Run

### Start the Backend (Flask)
```bash
cd ml_model
python app.py
```
*The server will run on `http://127.0.0.1:5001`.*

### Launch the Frontend
Simply open `frontend/index.html` in any modern web browser, or serve it using a local server:
```bash
cd frontend
# If you have Python installed:
python -m http.server 8000
```

## 📊 Data Generation
To generate a fresh set of sample reviews:
```bash
cd database_creator
python database_creator.py
```
This will create a `mobile_reviews_1000.csv` in the `output/` folder.

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
