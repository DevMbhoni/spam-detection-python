import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "training" / "SMSSpamCollection"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "spam_model.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(
        DATA_PATH,
        sep="\t",
        names=["label", "message"],
        encoding="latin-1",
    )

    df = df.dropna()
    df["label"] = df["label"].map({"ham": 0, "spam": 1})
    df["message"] = df["message"].astype(str)

    return df


def train_model() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()

    X = df["message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    max_features=5000,
                    ngram_range=(1, 2),
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    solver="liblinear",
                ),
            ),
        ]
    )

    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    report = classification_report(
        y_test,
        y_pred,
        target_names=["ham", "spam"],
        output_dict=True,
    )

    cm = confusion_matrix(y_test, y_pred).tolist()

    metadata = {
        "model_name": "TF-IDF + Logistic Regression",
        "dataset_source": "https://archive.ics.uci.edu/dataset/228/sms+spam+collection",
        "dataset_rows": int(len(df)),
        "features": "TF-IDF with unigrams and bigrams",
        "max_features": 5000,
        "test_size": 0.2,
        "random_state": 42,
        "metrics": {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
        },
        "classification_report": report,
        "confusion_matrix": cm,
    }

    joblib.dump(pipeline, MODEL_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print("Model saved to:", MODEL_PATH)
    print("Metadata saved to:", METADATA_PATH)
    print("Metrics:")
    print(json.dumps(metadata["metrics"], indent=2))


if __name__ == "__main__":
    train_model()