import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export const fetchScores = async () => {
    try {
        const { data } = await api.get('/scores/');
        return data;
    } catch (error) {
        console.error("Failed to fetch scores", error);
        return [];
    }
};

export const fetchTickerDetails = async (symbol) => {
    try {
        const { data } = await api.get(`/scores/${symbol}`);
        return data;
    } catch (error) {
        console.error(`Failed to fetch details for ${symbol}`, error);
        return null;
    }
};
