import json
from pathlib import Path

import joblib

from app.utils import (
    count_words,
    get_confidence,
    get_recommendation,
    get_risk_level,
    get_suspicious_words,
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "spam_model.joblib"
METADATA_PATH = BASE_DIR / "model" / "model_metadata.json"


model = joblib.load(MODEL_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)


def predict_message(text: str) -> dict:
    predicted_class = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    ham_probability = float(probabilities[0])
    spam_probability = float(probabilities[1])

    prediction = "spam" if predicted_class == 1 else "ham"

    main_probability = spam_probability if prediction == "spam" else ham_probability

    suspicious_words = get_suspicious_words(text)

    return {
        "prediction": prediction,
        "spam_probability": round(spam_probability, 4),
        "ham_probability": round(ham_probability, 4),
        "confidence": get_confidence(main_probability),
        "risk_level": get_risk_level(spam_probability),
        "suspicious_words": suspicious_words,
        "message_length": len(text),
        "word_count": count_words(text),
        "recommendation": get_recommendation(prediction, spam_probability),
        "model_used": metadata.get("model_name", "Unknown model"),
    }


def get_model_metadata() -> dict:
    return metadata