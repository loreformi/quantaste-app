const MacroOutlook = () => {
  const regions = [
    { name: 'Europa', score: 69, status: 'STAGFLAZIONE', color: 'bg-warning' },
    { name: 'Canada', score: 77, status: 'DEFLAZIONE', color: 'bg-danger' },
    { name: 'Cina', score: 41, status: 'REFLAZIONE', color: 'bg-success' },
    { name: 'Australia', score: 74, status: 'STAGFLAZIONE', color: 'bg-warning' },
  ];

  return (
    <div className="bg-dark-card p-6 rounded-lg text-light">
      <h3 className="text-xl font-bold mb-2">Regime Economico Predominante</h3>
      <p className="text-secondary text-sm mb-6">Indicazione del regime economico dominante attuale, basato su indicatori macroeconomici chiave.</p>

      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center">
            <span className="text-lg font-bold mr-2">America</span>
            <span className="bg-warning text-dark-card font-bold text-xs px-2 py-1 rounded">STAGFLAZIONE</span>
          </div>
          <div className="text-2xl font-bold">80<span className="text-secondary">/100</span></div>
        </div>
        <div className="w-full bg-dark-border rounded-full h-2.5">
          <div className="bg-gradient-to-r from-danger via-warning to-success h-2.5 rounded-full" style={{ width: '80%' }}></div>
        </div>
        <div className="text-right mt-2">
            <a href="#" className="text-primary text-sm font-semibold">Dettagli</a>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {regions.map(region => (
          <div key={region.name} className="bg-dark p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                    <span className="font-bold mr-2">{region.name}</span>
                    <span className={`${region.color} text-dark-card font-bold text-xs px-2 py-1 rounded`}>{region.status}</span>
                </div>
                <div className="text-xl font-bold">{region.score}<span className="text-secondary">/100</span></div>
            </div>
            <div className="text-right mt-2">
                <a href="#" className="text-primary text-sm font-semibold">Dettagli</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MacroOutlook;
