const Sentiment = () => {
  return (
    <div className="bg-dark-card p-6 rounded-lg text-light">
      <h3 className="text-xl font-bold mb-2">Smart Quant Sentiment</h3>
      <p className="text-secondary text-sm mb-6">Analisi del sentiment di mercato per tutte le asset class, basata sul modello Smart Quant.</p>

      <div className="flex justify-center mb-6">
        <div className="bg-dark-border p-1 rounded-lg flex space-x-1">
          <button className="px-4 py-1 bg-primary text-white rounded-md text-sm">Panoramica</button>
          <button className="px-4 py-1 text-secondary rounded-md text-sm">Dettagli</button>
        </div>
      </div>

      <div className="text-center mb-4">
        <div className="w-full bg-dark-border rounded-full h-2.5 mb-2">
            <div className="bg-gradient-to-r from-danger via-warning to-success h-2.5 rounded-full" style={{ width: '53%' }}></div>
        </div>
        <div className="flex justify-between text-xs text-secondary">
            <span>Sell</span>
            <span>Hold</span>
            <span>Buy</span>
        </div>
      </div>

      <div className="text-center my-8">
        <p className="text-7xl font-bold text-success">53%</p>
      </div>

      <div className="grid grid-cols-3 gap-4 text-center">
        <div>
          <p className="text-secondary">Sell</p>
          <p className="text-lg font-bold text-danger">↓ 27%</p>
        </div>
        <div>
          <p className="text-secondary">Hold</p>
          <p className="text-lg font-bold text-warning">20%</p>
        </div>
        <div>
          <p className="text-secondary">Buy</p>
          <p className="text-lg font-bold text-success">↑ 53%</p>
        </div>
      </div>
    </div>
  );
};

export default Sentiment;
