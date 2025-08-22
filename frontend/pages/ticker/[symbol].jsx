import { fetchTickerDetails } from '../../lib/api';
import ScoreChart from '../../components/ScoreChart';
import ScoreBadge from '../../components/ScoreBadge';
import Link from 'next/link';
import Header from '../../components/Header';

export async function getServerSideProps(context) {
    const { symbol } = context.params;
    const tickerDetails = await fetchTickerDetails(symbol.toUpperCase());

    if (!tickerDetails) {
        return { notFound: true };
    }

    return {
        props: { ticker: tickerDetails },
    };
}

const TickerPage = ({ ticker }) => {
    const latestScore = ticker.scores.length > 0 ? ticker.scores[ticker.scores.length - 1] : null;

    return (
        <div className="min-h-screen bg-dark">
            <Header />
            <div className="container mx-auto p-4 sm:p-6 lg:p-8">
                <header className="mb-8">
                    <Link href="/">
                        <span className="text-primary hover:text-blue-400">&larr; Back to Dashboard</span>
                    </Link>
                    <h1 className="text-4xl font-bold text-light mt-2">{ticker.company_name} ({ticker.symbol})</h1>
                    {latestScore && (
                        <div className="flex items-center space-x-4 mt-4">
                            <span className="text-5xl font-mono text-light">{latestScore.smoothed_score.toFixed(2)}</span>
                            <ScoreBadge label={latestScore.label} />
                        </div>
                    )}
                </header>

                <main className="bg-dark-card p-6 rounded-lg shadow-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-light">Smart Score Trend</h2>
                    <ScoreChart data={ticker.scores} />
                </main>
            </div>
        </div>
    );
};

export default TickerPage;