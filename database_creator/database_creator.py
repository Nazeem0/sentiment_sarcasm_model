import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

brands = [
    "Samsung Galaxy A54", "Samsung Galaxy S23", "iPhone 14", "iPhone 15",
    "Xiaomi Redmi Note 13", "Xiaomi 13 Pro", "OnePlus Nord CE 3",
    "OnePlus 11", "Realme Narzo 60", "Realme GT 6", "Vivo V27",
    "Vivo T2", "Oppo Reno 11", "Oppo A78", "Motorola Edge 40",
    "Motorola G84", "Nothing Phone 2", "Poco X6 Pro"
]

categories = ["Smartphone", "Mobile Phone", "Android Phone", "iOS Phone"]
languages = ["English", "Hinglish", "Hindi-English", "Tamil-English"]

positive_reviews = [
    "Battery life is amazing and lasts all day easily.",
    "Camera quality is excellent and photos come out very sharp.",
    "Performance is smooth and apps open quickly.",
    "The display is bright, clear, and enjoyable to use.",
    "Great value for money in this price range.",
    "The build quality feels premium and solid.",
    "Gaming works really well without much heating.",
    "Fingerprint sensor is fast and accurate.",
    "Charging is quick and the phone stays cool.",
    "Overall, a very reliable and satisfying phone."
]

negative_reviews = [
    "Battery drains too fast and barely lasts half a day.",
    "The phone gets laggy even during basic tasks.",
    "Camera quality is disappointing, especially in low light.",
    "Screen brightness is poor and hard to see outdoors.",
    "The device heats up too much after short use.",
    "Speaker quality is weak and distorted.",
    "Storage fills up too quickly for normal use.",
    "It keeps hanging and restarting randomly.",
    "Charging speed is slower than expected.",
    "Not worth the money at all."
]

sarcastic_reviews = [
    "Amazing phone, it freezes every time I open an app.",
    "Battery is excellent — it dies before lunch.",
    "Great camera if you enjoy blurry photos.",
    "So fast, I had time to make tea while it loaded.",
    "Premium feel, budget-level performance.",
    "Wonderful device, except for the constant heating.",
    "Perfect for gaming if you like watching lag.",
    "This phone really likes to restart itself for fun.",
    "A brilliant screen, if you only use it indoors.",
    "Fantastic performance, as long as you do nothing at all.",
    "Wow, such a great phone — it turned my calls into silence.",
    "Top-class device, because waiting is now my new hobby."
]

def make_row(i, label):
    brand = random.choice(brands)
    category = random.choice(categories)
    reviewer_id = f"R{random.randint(1000, 9999)}"
    product_id = f"P{10000 + i}"
    timestamp = (
        datetime(2024, 1, 1)
        + timedelta(days=random.randint(0, 700), minutes=random.randint(0, 1440))
    ).strftime("%Y-%m-%d %H:%M:%S")
    language_type = random.choice(languages)

    if label == "positive":
        review_text = random.choice(positive_reviews) + f" I liked the {brand}."
        rating = random.choice([4, 5])
    elif label == "negative":
        review_text = random.choice(negative_reviews) + f" My {brand} experience was bad."
        rating = random.choice([1, 2])
    else:
        review_text = random.choice(sarcastic_reviews) + f" I am talking about the {brand}."
        rating = random.choice([1, 2])

    return {
        "product_id": product_id,
        "product_name": brand,
        "category": category,
        "review_text": review_text,
        "rating": rating,
        "timestamp": timestamp,
        "reviewer_id": reviewer_id,
        "language_type": language_type
    }

labels = ["positive"] * 350 + ["negative"] * 350 + ["sarcastic"] * 300
random.shuffle(labels)

rows = [make_row(i, label) for i, label in enumerate(labels)]
df = pd.DataFrame(rows)

ordered_cols = [
    "product_id",
    "product_name",
    "category",
    "review_text",
    "rating",
    "timestamp",
    "reviewer_id",
    "language_type"
]

df = df[ordered_cols]

os.makedirs("output", exist_ok=True)
df.to_csv("output/mobile_reviews_1000.csv", index=False)

print("Saved: output/mobile_reviews_1000.csv")
print(df.shape)
print(df.head())