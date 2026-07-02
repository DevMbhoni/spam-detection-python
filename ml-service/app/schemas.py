from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Email, SMS, or message text to classify.",
    )


class PredictionResponse(BaseModel):
    prediction: str
    spam_probability: float
    ham_probability: float
    confidence: str
    risk_level: str
    suspicious_words: list[str]
    message_length: int
    word_count: int
    recommendation: str
    model_used: str