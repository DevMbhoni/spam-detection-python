export type PredictionResponse = {
    prediction: "spam" | "ham";
    spam_probability: number;
    ham_probability: number;
    confidence: "Low" | "Medium" | "High";
    risk_level: "Low" | "Medium" | "High";
    suspicious_words: string[];
    message_length: number;
    word_count: number;
    recommendation: string;
    model_used: string;
};