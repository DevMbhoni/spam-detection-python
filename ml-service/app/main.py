from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.predict import get_model_metadata, predict_message
from app.schemas import PredictionRequest, PredictionResponse


app = FastAPI(
    title="Spam Detection ML Service",
    description="A FastAPI service for detecting spam or ham messages using a trained ML model.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Spam Detection ML Service is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/metadata")
def metadata():
    return get_model_metadata()


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    return predict_message(request.text)