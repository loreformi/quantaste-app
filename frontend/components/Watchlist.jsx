import { MagnifyingGlassIcon, LockClosedIcon } from '@heroicons/react/24/outline';

const Watchlist = () => {
  const assets = [
    { name: 'FTNT', company: 'Fortinet I...', change: '-2.97%', changeType: 'negative' },
    { name: 'CYBR', company: 'CyberArk S...', change: '-0.53%', changeType: 'negative' },
    { name: 'AMZN', company: 'Amazon.com...', change: '-0.39%', changeType: 'negative' },
    { name: 'MEOH', company: 'Methanex C...', change: '-1.78%', changeType: 'negative' },
  ];

  const macroEvents = [
    { name: 'Consumer Confidence (Aug)', time: '02:00', est: '65', act: '-' },
    { name: 'Industrial Profits YoY (Jul)', time: '01:30', est: '-1.8', act: '-' },
    { name: 'Monthly CPI Indicator (Jul)', time: '01:30', est: '2.3', act: '-' },
    { name: 'Construction Work Done QoQ (Q2)', time: '01:30', est: '1.2', act: '-' },
  ];

  return (
    <div className="bg-dark-card p-4 rounded-lg text-light h-full">
      <h2 className="text-xl font-bold mb-4">Watchlist</h2>
      <div className="relative mb-4">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-secondary" />
        <input 
          type="text" 
          placeholder="Search assets..." 
          className="bg-dark w-full pl-10 pr-4 py-2 rounded-lg border border-dark-border focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
      <div className="flex space-x-2 mb-4">
        {['All', 'Stocks', 'Forex', 'Crypto', 'Index', 'ETF'].map(filter => (
          <button key={filter} className={`px-3 py-1 rounded-md text-sm ${filter === 'All' ? 'bg-primary text-white' : 'bg-dark-border text-secondary'}`}>
            {filter}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {assets.map(asset => (
          <div key={asset.name} className="grid grid-cols-4 items-center text-sm">
            <div>
              <p className="font-bold">{asset.name}</p>
              <p className="text-secondary">{asset.company}</p>
            </div>
            <div className={`text-right ${asset.changeType === 'negative' ? 'text-danger' : 'text-success'}`}>
              {asset.change}
            </div>
            <div className="flex justify-center">
              <LockClosedIcon className="w-5 h-5 text-secondary" />
            </div>
            <div className="flex justify-center">
              <LockClosedIcon className="w-5 h-5 text-secondary" />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-bold mb-2">Macro & Earnings</h3>
        <p className="text-secondary text-sm mb-4">Macro events and Earnings reports on 26 August</p>
        <div className="flex space-x-2 mb-4">
          <button className="px-3 py-1 rounded-md text-sm bg-primary text-white">News</button>
          <button className="px-3 py-1 rounded-md text-sm bg-dark-border text-secondary">Earnings</button>
        </div>
        <div className="space-y-3">
          {macroEvents.map(event => (
            <div key={event.name} className="flex items-center justify-between text-sm">
              <div>
                <p>{event.name}</p>
                <p className="text-secondary">Est: {event.est} | Act: {event.act}</p>
              </div>
              <div className="text-secondary bg-dark-border px-2 py-1 rounded-md">{event.time}</div>
            </div>
          ))}
        </div>
        <div className="text-center mt-4">
            <a href="#" className="text-primary text-sm font-semibold">See all news</a>
        </div>
      </div>
    </div>
  );
};

export default Watchlist;
