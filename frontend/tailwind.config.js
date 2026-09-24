/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#bae0fd',
          300: '#7cc8fc',
          400: '#36abf8',
          500: '#0c8fe9',
          600: '#0271c7',
          700: '#035aa1',
          800: '#074c85',
          900: '#0c406e',
          950: '#082849',
        },
        navy: {
          800: '#0f2744',
          900: '#0a192f',
          950: '#060d19',
        },
        gold: {
          400: '#e5b945',
          500: '#c59b27',
          600: '#9d7616',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['Merriweather', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      }
    },
  },
  plugins: [],
}
