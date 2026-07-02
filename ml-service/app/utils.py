import re


SUSPICIOUS_KEYWORDS = [
    "free",
    "win",
    "winner",
    "prize",
    "claim",
    "urgent",
    "cash",
    "bonus",
    "click",
    "offer",
    "selected",
    "congratulations",
    "guaranteed",
    "limited",
    "deal",
    "reward",
    "lottery",
    "credit",
    "loan",
    "verify",
    "account",
    "password",
    "bank",
]


def get_suspicious_words(text: str) -> list[str]:
    text_lower = text.lower()

    found = []
    for keyword in SUSPICIOUS_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"
        if re.search(pattern, text_lower):
            found.append(keyword)

    return found


def get_confidence(probability: float) -> str:
    if probability >= 0.85:
        return "High"
    if probability >= 0.65:
        return "Medium"
    return "Low"


def get_risk_level(spam_probability: float) -> str:
    if spam_probability >= 0.80:
        return "High"
    if spam_probability >= 0.50:
        return "Medium"
    return "Low"


def get_recommendation(prediction: str, spam_probability: float) -> str:
    if prediction == "spam" and spam_probability >= 0.80:
        return "This message looks risky. Do not click links, send money, or share personal information."

    if prediction == "spam":
        return "This message may be spam. Review it carefully before taking action."

    if spam_probability >= 0.40:
        return "This message was classified as ham, but it has some suspicious signals. Review it carefully."

    return "This message appears legitimate based on the model prediction."


def count_words(text: str) -> int:
    return len(text.split())