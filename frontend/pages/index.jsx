import Header from '../components/Header';
import Watchlist from '../components/Watchlist';
import MacroOutlook from '../components/MacroOutlook';
import Sentiment from '../components/Sentiment';
import Proposte from '../components/Proposte';

export default function Home() {
    return (
        <div className="min-h-screen bg-dark text-light">
            <Header />
            <div className="flex">
                <aside className="w-1/4 p-4">
                    <Watchlist />
                </aside>
                <main className="w-3/4 p-4">
                    <h1 className="text-2xl font-bold mb-4">Macro and Markets Outlook</h1>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <MacroOutlook />
                        <Sentiment />
                    </div>
                    <div className="mt-4">
                        <Proposte />
                    </div>
                </main>
            </div>
        </div>
    );
}