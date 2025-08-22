import { fetchScores } from '../lib/api';
import TickerTable from '../components/TickerTable';
import Header from '../components/Header';

export async function getServerSideProps() {
    const tickers = await fetchScores();
    // Sort tickers by symbol for consistent ordering
    const sortedTickers = tickers.sort((a, b) => a.symbol.localeCompare(b.symbol));
    return {
        props: { tickers: sortedTickers },
    };
}

export default function Home({ tickers }) {
    return (
        <div className="min-h-screen bg-dark">
            <Header />
            <div className="container mx-auto p-4 sm:p-6 lg:p-8">
                <header className="mb-8">
                    <h1 className="text-4xl font-bold text-light">Smart Score Dashboard</h1>
                    <p className="text-lg text-secondary">Overview of market opportunities.</p>
                </header>
                <main>
                    <TickerTable tickers={tickers} />
                </main>
                <footer className="text-center mt-12 text-secondary">
                    <p>Data provided by Yahoo Finance. For educational purposes only.</p>
                </footer>
            </div>
        </div>
    );
}