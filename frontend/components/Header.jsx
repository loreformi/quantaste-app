import React from 'react';
import Link from 'next/link';
import { MagnifyingGlassIcon, GlobeAltIcon, UserCircleIcon, BellIcon, CogIcon, SunIcon } from '@heroicons/react/24/outline';

const Header = () => {
  return (
    <header className="bg-dark-card text-light p-4 shadow-md flex justify-between items-center">
      <div className="flex items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
      </div>

      <div className="flex-1 flex justify-center items-center">
        <nav className="flex items-center space-x-6">
          <Link href="/"><span className="font-bold text-xl">Quantaste</span></Link>
          <Link href="/"><span className="text-secondary hover:text-light">Radar</span></Link>
          <Link href="/"><span className="text-secondary hover:text-light">Paesi</span></Link>
          <Link href="/"><span className="text-secondary hover:text-light">Blog</span></Link>
          <Link href="/"><span className="text-secondary hover:text-light">Formazione</span></Link>
          <Link href="/"><span className="text-secondary hover:text-light">News and Macro</span></Link>
        </nav>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-secondary" />
          <input 
            type="text" 
            placeholder="Cosa stai cercando?" 
            className="bg-dark pl-10 pr-4 py-2 rounded-lg border border-dark-border focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <button className="p-2 rounded-full hover:bg-dark-border">
          <GlobeAltIcon className="w-6 h-6 text-secondary" />
        </button>
        <button className="p-2 rounded-full hover:bg-dark-border">
          <UserCircleIcon className="w-6 h-6 text-secondary" />
        </button>
      </div>
    </header>
  );
};

export default Header;