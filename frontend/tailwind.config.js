/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0D1117',
        'dark-card': '#161B22',
        'dark-border': '#30363D',
        primary: '#58A6FF',
        secondary: '#8B949E',
        success: '#3FB950',
        danger: '#F85149',
        warning: '#D29922',
        light: '#C9D1D9',
        white: '#FFFFFF',
      },
    },
  },
  plugins: [],
}