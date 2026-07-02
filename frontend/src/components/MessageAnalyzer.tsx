import { useState } from "react";
import { Loader2, SearchCheck } from "lucide-react";
import { predictSpam } from "../api/spamApi";
import type { PredictionResponse } from "../types/prediction";
import { PredictionCard } from "./PredictionCard";

const sampleSpam =
    "Congratulations! You have won a free prize. Claim now by clicking this link.";

const sampleHam =
    "Hi, just checking if we are still meeting at 5 today.";

export function MessageAnalyzer() {
    const [message, setMessage] = useState("");
    const [result, setResult] = useState<PredictionResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleAnalyze() {
        if (!message.trim()) {
            setError("Please paste a message first.");
            return;
        }

        try {
            setLoading(true);
            setError("");
            setResult(null);

            const prediction = await predictSpam(message);
            setResult(prediction);
        } catch (err) {
            setError(
                "Could not connect to the ML service. Make sure FastAPI is running on port 8000."
            );
        } finally {
            setLoading(false);
        }
    }

    function useSample(text: string) {
        setMessage(text);
        setResult(null);
        setError("");
    }

    return (
        <main className="page">
            <section className="hero">
                <p className="eyebrow">Machine Learning Spam Detection</p>
                <h1>Email & SMS Spam Checker</h1>
                <p className="hero-text">
                    Paste a message below and the model will classify it as spam or ham,
                    show probability scores, suspicious words, risk level, and a safety
                    recommendation.
                </p>
            </section>

            <section className="analyzer-card">
                <label htmlFor="message">Message text</label>

                <textarea
                    id="message"
                    placeholder="Paste an email, SMS, or message here..."
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                />

                <div className="actions">
                    <button onClick={handleAnalyze} disabled={loading}>
                        {loading ? (
                            <>
                                <Loader2 className="button-icon spinning" />
                                Analyzing...
                            </>
                        ) : (
                            <>
                                <SearchCheck className="button-icon" />
                                Analyze message
                            </>
                        )}
                    </button>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={() => useSample(sampleSpam)}
                    >
                        Try spam sample
                    </button>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={() => useSample(sampleHam)}
                    >
                        Try ham sample
                    </button>
                </div>

                {error && <p className="error">{error}</p>}
            </section>

            {result && <PredictionCard result={result} />}
        </main>
    );
}