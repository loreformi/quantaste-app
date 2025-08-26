const Proposte = () => {
  return (
    <div className="bg-dark-card p-6 rounded-lg text-light">
      <h3 className="text-xl font-bold mb-2">Proposte del giorno</h3>
      <p className="text-secondary text-sm mb-6">Selezione dei 3 asset con il maggior vantaggio statistico.</p>
      <div className="bg-dark p-4 rounded-lg flex items-center space-x-4">
        <div className="bg-teal-500 p-4 rounded-lg">
          <span className="text-2xl font-bold text-white">IN</span>
        </div>
        <div>
          <p className="text-lg font-bold">Interpump Group S.p.A (IP)</p>
        </div>
      </div>
    </div>
  );
};

export default Proposte;
