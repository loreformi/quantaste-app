import React from 'react';
import Link from 'next/link';
import ScoreBadge from './ScoreBadge';

const TickerTable = ({ tickers }) => {
    if (!tickers || tickers.length === 0) {
        return <p className="text-center text-secondary">No ticker data available. The backend might be initializing.</p>;
    }

    return (
        <div className="overflow-x-auto bg-dark-card rounded-lg shadow-lg p-4">
            <table className="min-w-full">
                <thead>
                    <tr className="border-b border-dark-border">
                        <th className="px-6 py-3 text-left text-xs font-medium text-secondary uppercase tracking-wider">Ticker</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-secondary uppercase tracking-wider">Company Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-secondary uppercase tracking-wider">Smart Score</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-secondary uppercase tracking-wider">Label</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-dark-border">
                    {tickers.map((ticker) => (
                        <tr key={ticker.id} className="hover:bg-dark-border transition-colors duration-150">
                            <td className="px-6 py-4 whitespace-nowrap">
                                <Link href={`/ticker/${ticker.symbol}`}>
                                    <span className="font-bold text-lg text-primary hover:text-blue-400 cursor-pointer">{ticker.symbol}</span>
                                </Link>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-light">{ticker.company_name}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`font-mono text-lg ${ticker.latest_score?.smoothed_score >= 65 ? 'text-success' : ticker.latest_score?.smoothed_score >= 45 ? 'text-warning' : 'text-danger'}`}>
                                    {ticker.latest_score ? ticker.latest_score.smoothed_score.toFixed(2) : 'N/A'}
                                </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <ScoreBadge label={ticker.latest_score?.label} />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TickerTable;