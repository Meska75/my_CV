/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        bg: '#07070c',
        bg2: '#0e0e16',
        surface: '#14141f',
        surface2: '#1c1c2a',
        line: '#2a2a3d',
        ink: '#f4f0ea',
        cream: '#e8dcc8',
        muted: '#9490a8',
        accent: '#b794f6',
        accent2: '#6ee7b7',
        hot: '#fb7185',
      },
      fontFamily: {
        sans: ['Vazirmatn', 'system-ui', 'sans-serif'],
        display: ['Estedad', 'Vazirmatn', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      maxWidth: {
        prose: '65ch',
        site: '76rem',
      },
      boxShadow: {
        glow: '0 0 50px -10px rgba(183,148,246,.45)',
        'glow-lg': '0 0 70px -8px rgba(183,148,246,.55)',
        'glow-mint': '0 0 40px -10px rgba(110,231,183,.35)',
        card: '0 8px 32px -8px rgba(0,0,0,.55)',
        inner: 'inset 0 1px 0 rgba(255,255,255,.06)',
      },
      animation: {
        float: 'float 7s ease-in-out infinite',
        'float-delayed': 'float 7s ease-in-out 2s infinite',
        marquee: 'marquee 28s linear infinite',
        shimmer: 'shimmer 4s ease-in-out infinite',
        blink: 'blink 1s step-end infinite',
        'mesh-drift': 'meshDrift 18s ease-in-out infinite alternate',
        'spin-slow': 'spin 24s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        shimmer: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
        meshDrift: {
          '0%': { transform: 'translate(0, 0) scale(1)' },
          '100%': { transform: 'translate(3%, -2%) scale(1.06)' },
        },
      },
    },
  },
  plugins: [],
};
