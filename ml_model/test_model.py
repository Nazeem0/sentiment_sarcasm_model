from transformers import pipeline
import os

MODEL_PATH = os.path.join(os.getcwd(), "sentiment_sarcasm_model")
print("Loading model from:", MODEL_PATH)

try:
    classifier = pipeline("text-classification", model=MODEL_PATH, tokenizer=MODEL_PATH)
    print("Model loaded successfully.")
    texts = [
        "This is a great product!",
        "worst experience ever",
        "The battery lasts for 2 minutes, amazing engineering.",
        "Phone acha hai but price thoda zyada hai."
    ]
    results = classifier(texts)
    for t, r in zip(texts, results):
        print(f"Text: {t}")
        print(f"Result: {r}")
except Exception as e:
    print(f"Error: {e}")
