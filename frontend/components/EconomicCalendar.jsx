import React, { useEffect, useState } from 'react';

const EconomicCalendar = () => {
  const [calendarData, setCalendarData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("EconomicCalendar useEffect triggered"); // Added for debugging
    const fetchCalendarData = async () => {
      try {
        const response = await fetch('/api/economic-calendar');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setCalendarData(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCalendarData();
  }, []);

  if (loading) {
    return <div className="text-white">Caricamento calendario economico...</div>;
  }

  if (error) {
    return <div className="text-red-500">Errore nel caricamento del calendario: {error}</div>;
  }

  if (calendarData.length === 0) {
    return <div className="text-white">Nessun evento del calendario economico trovato per il periodo selezionato.</div>;
  }

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-white mb-4">Calendario Economico</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-700">
            <tr>
              <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Data</th>
              <th scope="col" className="px-4 py-2 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Evento</th>
            </tr>
          </thead>
          <tbody className="bg-gray-800 divide-y divide-gray-700">
            {calendarData.map((event, index) => (
              <tr key={index}>
                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-200">{new Date(event.Date).toLocaleDateString()}</td>
                <td className="px-4 py-2 text-sm text-gray-200">{event.Event}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EconomicCalendar;