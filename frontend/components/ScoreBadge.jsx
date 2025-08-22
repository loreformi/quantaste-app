import React from 'react';

const getBadgeColor = (label) => {
    switch (label) {
        case 'Strong Buy':
            return 'bg-success text-light';
        case 'Buy':
            return 'bg-green-600 text-light'; // Slightly darker green for 'Buy'
        case 'Neutral':
            return 'bg-secondary text-light';
        case 'Sell':
            return 'bg-danger text-light';
        case 'Strong Sell':
            return 'bg-red-700 text-light'; // Slightly darker red for 'Strong Sell'
        default:
            return 'bg-dark-border text-light';
    }
};

const ScoreBadge = ({ label }) => {
    if (!label) return null;

    return (
        <span className={`px-3 py-1 text-sm font-semibold rounded-md ${getBadgeColor(label)}`}>
            {label}
        </span>
    );
};

export default ScoreBadge;