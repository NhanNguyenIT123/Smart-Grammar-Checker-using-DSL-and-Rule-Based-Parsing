/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'lime': '#B9FF66',
        'light-gray': '#F3F3F3',
        'dark': '#191A23',
        'black': '#000000',
      },
      fontFamily: {
        'grotesk': ['Space Grotesk', 'sans-serif'],
      },
      spacing: {
        'section': '5rem',
      },
    },
  },
  plugins: [],
}
