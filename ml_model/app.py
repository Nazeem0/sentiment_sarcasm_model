from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# Path to your local model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "sentiment_sarcasm_model")

# Load model pipeline
print("Loading model from:", MODEL_PATH)
try:
    classifier = pipeline("text-classification", model=MODEL_PATH, tokenizer=MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    classifier = None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are supported"}), 400

    try:
        df = pd.read_csv(file)
        
        # Determine which column to use for text
        text_column = None
        if 'review_text' in df.columns:
            text_column = 'review_text'
        else:
            # Fallback: try to find a column with strings
            for col in df.columns:
                if df[col].dtype == object and isinstance(df[col].iloc[0], str):
                    text_column = col
                    # Pick the longest string column usually
                    break
        
        if not text_column:
            return jsonify({"error": "Could not find a text column in the CSV"}), 400
        
        results = {
            "positive": [],
            "negative": [],
            "sarcastic": []
        }

        # Process the rows
        # We handle up to 100 rows to avoid long inference times in demo, adjust as needed
        texts = df[text_column].dropna().astype(str).tolist()
        
        # Increased limit to handle the full dataset
        MAX_ROWS = 2000
        if len(texts) > MAX_ROWS:
            texts = texts[:MAX_ROWS]

        if classifier is None:
            return jsonify({"error": "Model failed to load on the server."}), 500

        # Processing in batches to speed up inference
        predictions = classifier(texts, batch_size=32)
        
        for text, pred in zip(texts, predictions):
            label = pred['label'].lower()
            score = round(pred['score'], 4)
            
            # Map LABEL_X to human readable strings if needed
            mapped_label = label
            if label == 'label_0':
                mapped_label = 'negative'
            elif label == 'label_1':
                mapped_label = 'positive'
            elif label == 'label_2':
                mapped_label = 'sarcastic'
            
            # Enhanced Sentiment Logic
            positive_keywords = ['amazing', 'excellent', 'great', 'wonderful', 'perfect', 'love', 'best', 'top-class', 'fantastic', 'superb', 'premium', 'reliable', 'satisfying', 'fast']
            negative_keywords = ['bad', 'worst', 'terrible', 'hate', 'awful', 'disappointing', 'horrible', 'poor', 'slow', 'freeze', 'hang', 'broken', 'die']
            
            has_positive = any(word in text.lower() for word in positive_keywords)
            has_negative = any(word in text.lower() for word in negative_keywords)
            has_contrast = any(word in text.lower() for word in ['but', 'except', 'however', 'only if', 'as long as'])
            
            if mapped_label == 'negative':
                if has_positive and not has_negative:
                    mapped_label = 'positive' # Positive Override
                elif has_positive and (has_negative or has_contrast):
                    mapped_label = 'sarcastic' # True Sarcasm

            item = {
                "text": text,
                "score": score,
                "original_label": mapped_label
            }

            if mapped_label == 'positive':
                results["positive"].append(item)
            elif mapped_label == 'negative':
                results["negative"].append(item)
            elif mapped_label == 'sarcastic':
                results["sarcastic"].append(item)
            else:
                results["sarcastic"].append(item)

        return jsonify(results)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_single():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    if classifier is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        pred = classifier(text)[0]
        print(f"Prediction for '{text}': {pred}")
        label = pred['label'].lower()
        score = round(pred['score'], 4)
        
        mapped_label = label
        if label == 'label_0':
            mapped_label = 'negative'
        elif label == 'label_1':
            mapped_label = 'positive'
        elif label == 'label_2':
            mapped_label = 'sarcastic'
        
        # Enhanced Sentiment Logic
        positive_keywords = ['amazing', 'excellent', 'great', 'wonderful', 'perfect', 'love', 'best', 'top-class', 'fantastic', 'superb', 'premium', 'reliable', 'satisfying', 'fast']
        negative_keywords = ['bad', 'worst', 'terrible', 'hate', 'awful', 'disappointing', 'horrible', 'poor', 'slow', 'freeze', 'hang', 'broken', 'die']
        
        has_positive = any(word in text.lower() for word in positive_keywords)
        has_negative = any(word in text.lower() for word in negative_keywords)
        has_contrast = any(word in text.lower() for word in ['but', 'except', 'however', 'only if', 'as long as'])
        
        if mapped_label == 'negative':
            if has_positive and not has_negative:
                mapped_label = 'positive' # Positive Override
            elif has_positive and (has_negative or has_contrast):
                mapped_label = 'sarcastic' # True Sarcasm
            
        return jsonify({
            "text": text,
            "label": mapped_label,
            "score": score
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
