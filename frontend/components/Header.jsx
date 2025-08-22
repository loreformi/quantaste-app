import React from 'react';
import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-dark-card text-light p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/">
          <span className="text-2xl font-bold text-primary cursor-pointer">
            Quantaste
          </span>
        </Link>
        <nav>
          {/* Add navigation links here if needed */}
        </nav>
      </div>
    </header>
  );
};

export default Header;
