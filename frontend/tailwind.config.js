/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          DEFAULT: '#1a1a1a', // Main background
          card: '#2a2a2a', // Card background
          border: '#3a3a3a', // Border color
        },
        primary: '#007bff', // Blue for interactive elements
        secondary: '#6c757d', // Grey for secondary text
        success: '#28a745', // Green for positive
        warning: '#ffc107', // Yellow/Orange for neutral/warning
        danger: '#dc3545', // Red for negative
        info: '#17a2b8', // Info blue
        light: '#f8f9fa', // Light text
        darktext: '#343a40', // Dark text on light backgrounds
      },
    },
  },
  plugins: [],
}