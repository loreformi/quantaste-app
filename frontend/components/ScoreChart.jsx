import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ScoreChart = ({ data }) => {
    return (
        <div style={{ width: '100%', height: 400 }}>
            <ResponsiveContainer>
                <LineChart
                    data={data}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#3a3a3a" /> {/* Use dark-border */}
                    <XAxis dataKey="date" stroke="#6c757d" /> {/* Use secondary color */}
                    <YAxis domain={[0, 100]} stroke="#6c757d" /> {/* Use secondary color */}
                    <Tooltip
                        contentStyle={{ backgroundColor: '#2a2a2a', border: '1px solid #3a3a3a' }} // Use dark-card and dark-border
                        labelStyle={{ color: '#f8f9fa' }} // Use light color
                    />
                    <Legend wrapperStyle={{ color: '#f8f9fa' }} /> {/* Use light color */}
                    <Line type="monotone" dataKey="smoothed_score" name="Smart Score (Smoothed)" stroke="#28a745" strokeWidth={2} dot={false} /> {/* Use success color */}
                    <Line type="monotone" dataKey="final_score" name="Daily Score" stroke="#007bff" strokeWidth={1} activeDot={{ r: 8 }} /> {/* Use primary color */}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ScoreChart;