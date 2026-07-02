import {
    AlertTriangle,
    CheckCircle,
    ShieldAlert,
    Activity,
    MessageSquareText,
    ScanSearch,
} from "lucide-react";
import type { PredictionResponse } from "../types/prediction";

type PredictionCardProps = {
    result: PredictionResponse;
};

function percentage(value: number) {
    return `${Math.round(value * 100)}%`;
}

export function PredictionCard({ result }: PredictionCardProps) {
    const isSpam = result.prediction === "spam";

    const predictionLabel = isSpam ? "Spam" : "Ham";
    const predictionIcon = isSpam ? (
        <ShieldAlert className="icon danger" />
    ) : (
        <CheckCircle className="icon success" />
    );

    return (
        <section className="result-card">
            <div className="result-header">
                <div>
                    <p className="eyebrow">Prediction result</p>
                    <h2 className={isSpam ? "danger-text" : "success-text"}>
                        {predictionIcon}
                        {predictionLabel}
                    </h2>
                </div>

                <span className={`badge ${isSpam ? "badge-danger" : "badge-success"}`}>
                    {result.confidence} confidence
                </span>
            </div>

            <div className="probability-section">
                <div className="probability-row">
                    <span>Spam probability</span>
                    <strong>{percentage(result.spam_probability)}</strong>
                </div>
                <div className="progress-track">
                    <div
                        className="progress-fill spam-fill"
                        style={{ width: percentage(result.spam_probability) }}
                    />
                </div>

                <div className="probability-row">
                    <span>Ham probability</span>
                    <strong>{percentage(result.ham_probability)}</strong>
                </div>
                <div className="progress-track">
                    <div
                        className="progress-fill ham-fill"
                        style={{ width: percentage(result.ham_probability) }}
                    />
                </div>
            </div>

            <div className="details-grid">
                <div className="detail-box">
                    <Activity className="small-icon" />
                    <span>Risk level</span>
                    <strong>{result.risk_level}</strong>
                </div>

                <div className="detail-box">
                    <MessageSquareText className="small-icon" />
                    <span>Words</span>
                    <strong>{result.word_count}</strong>
                </div>

                <div className="detail-box">
                    <ScanSearch className="small-icon" />
                    <span>Characters</span>
                    <strong>{result.message_length}</strong>
                </div>
            </div>

            <div className="recommendation">
                <AlertTriangle className="small-icon" />
                <p>{result.recommendation}</p>
            </div>

            <div className="suspicious-section">
                <h3>Suspicious words detected</h3>

                {result.suspicious_words.length > 0 ? (
                    <div className="keyword-list">
                        {result.suspicious_words.map((word) => (
                            <span key={word} className="keyword">
                                {word}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p className="muted">No suspicious keywords were detected.</p>
                )}
            </div>

            <p className="model-used">Model used: {result.model_used}</p>
        </section>
    );
}