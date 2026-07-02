import axios from "axios";
import type { PredictionResponse } from "../types/prediction";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function predictSpam(text: string): Promise<PredictionResponse> {
    const response = await axios.post<PredictionResponse>(
        `${API_BASE_URL}/predict`,
        { text }
    );

    return response.data;
}