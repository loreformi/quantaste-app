import Header from '../components/Header';
import Watchlist from '../components/Watchlist';
import MacroOutlook from '../components/MacroOutlook';
import Sentiment from '../components/Sentiment';
import Proposte from '../components/Proposte';
import EconomicCalendar from '../components/EconomicCalendar';
import { fetchDashboardData, fetchTickers } from '../lib/api';

export async function getServerSideProps() {
    const dashboardData = await fetchDashboardData();
    const tickers = await fetchTickers();
    return {
        props: {
            dashboardData,
            tickers,
        },
    };
}

export default function Home({ dashboardData, tickers }) {
    return (
        <div className="min-h-screen bg-dark text-light">
            <Header />
            <div className="flex">
                <aside className="w-1/4 p-4">
                    <Watchlist tickers={tickers} />
                </aside>
                <main className="w-3/4 p-4">
                    <h1 className="text-2xl font-bold mb-4">Macro and Markets Outlook</h1>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <MacroOutlook data={dashboardData?.economic_regimes} />
                        <Sentiment data={dashboardData?.market_sentiment} />
                    </div>
                    <div className="mt-4">
                        <Proposte data={dashboardData?.daily_picks} />
                    </div>
                    {/* New Economic Calendar Section */}
                    <div className="mt-4">
                        <EconomicCalendar />
                    </div>
                </main>
            </div>
        </div>
    );
}
